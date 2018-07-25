#!/usr/bin/env python

import os
import subprocess

import rospy
import rosnode
from std_srvs.srv import Trigger, TriggerResponse
from data_recording.srv import Record, RecordResponse


class DataRecorder():
    def __init__(self):
        self.start_recording_service = rospy.Service('/data_recording/start_recording', Record, self.start_recording)
        self.stop_recording_service = rospy.Service('/data_recording/stop_recording', Trigger, self.stop_recording)
        self.stop_recording_service = rospy.Service('/data_recording/toggle_recording', Trigger, self.toggle_recording)

        self.process = None
        self.recording = False

        self.output_directory = rospy.get_param('/data_recording/output_directory', '~/rosbag/')

        self.topics = rospy.get_param('/data_recording/topics', [])
        if not self.topics:
            rospy.logerr('No Topics Specified.')
        self.command = None

        rospy.loginfo('Data Recorder Started')

    def toggle_recording(self, req):
        if self.recording:
            return self.stop_recording(req)
        else:
            return self.start_recording(req)

    def start_recording(self, req):
        if self.recording:
            rospy.logerr('Already Recording')
            return RecordResponse(False, 'Already Recording')

        self.bagname = req.bagname
        if self.bagname != '':
            command = ['rosrun', 'rosbag', 'record', '-e', '-O', self.bagname] + self.topics + \
                      ['__name:=data_recording_myrecorder']
        else: # default to datetime bag name
            command = ['rosrun', 'rosbag', 'record', '-e'] + self.topics + \
                      ['__name:=data_recording_myrecorder']
        self.process = subprocess.Popen(command, cwd=self.output_directory)
        self.recording = True
        rospy.loginfo('Started recorder, PID %s' % self.process.pid)
        return RecordResponse(True, 'Started recorder, PID %s' % self.process.pid)

    def stop_recording(self, req):
        if not self.recording:
            rospy.logerr('Not Recording')
            return TriggerResponse(False, 'Not Recording')

        rosnode.kill_nodes(['/data_recording_myrecorder'])

        self.process = None
        self.recording = False

        rospy.loginfo('Stopped Recording, Compressing...')

        # open a subprocess for compressing the bag
        bag_path = self.output_directory + '/' + self.bagname
        compr_command = ['rosbag', 'compress',
                         bag_path + '.bag', '--output-dir', self.output_directory]
        result = subprocess.call(compr_command)

        if result == 0:  # compression succeeded
            subprocess.call(['rm', bag_path + '.orig.bag'])
            rospy.loginfo('Compression successful')
        else:
            rospy.logerr('Compression failed')

        return TriggerResponse(True, 'Stopped Recording')


if __name__ == "__main__":
    rospy.init_node('data_recording')
    DataRecorder()
    rospy.spin()
