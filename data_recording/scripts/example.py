#! /usr/bin/env python
# Example of how to use the recording services
# This assumes other relevant nodes you want to record are launched
import rospy

from std_srvs.srv import Trigger, TriggerRequest
from visualization_msgs.msg import Marker


def something_interesting():
    """Dummy thing that takes up time"""
    global annotation_pub

    rospy.sleep(1)

    text_marker = Marker()
    text_marker.header.stamp = rospy.get_rostime()
    text_marker.header.frame_id = "/world" # You can also put text on say the end effector!
    text_marker.type = 9  # this specifies that the marker is a text marker
    text_marker.pose.position = {x: 0.0, y: 0.0, z: 0.0}
    text_marker.pose.orientation = {x: 0.0, y: 0.0, z: 0.0, w: 0.0}
    text_marker.scale = {x: 0.5, y: 0.5, z: 0.5} # units?
    text_marker.color = {r: 1.0, g: 0.0, b: 0.0, a: 1.0} # make sure 'a' is set to >0, otherwise invisible
    text_marker.lifetime = {secs: 2, nsecs: 0}
    text_marker.text = "This should appear after one second and last 2 seconds"

    rospy.sleep(3)
    text_marker.pose.position = {x: 1.0, y: 1.0, z: 1.0}
    text_marker.scale = {x: 1, y: 1, z: 1}
    text_marker.color = {r: 0.0, g: 0.5, b: 0.5, a: 1.0}
    text_marker.lifetime = {secs: 1, nsecs: 200}
    text_marker.text = "hello world"
    annotation_pub.publish(text_marker)

    rospy.sleep(3)
    text_marker.pose.position = {x: 0.0, y: 0.0, z: 1.0}
    text_marker.scale = {x: 0.3, y: 0.3, z: 0.3}
    text_marker.color = {r: 0.3, g: 0.7, b: 0.0, a: 1.0}
    text_marker.lifetime = {secs: 1, nsecs: 200}
    text_marker.text = "Testing last marker"
    annotation_pub.publish(text_marker)


if __name__ == '__main__':
    rospy.init_node('recording_example')

    start_record_srv = rospy.ServiceProxy('/data_recording/start_recording', Trigger)
    stop_record_srv = rospy.ServiceProxy('/data_recording/stop_recording', Trigger)

    annotation_pub = rospy.Publisher('/data_recording/annotations', Marker, queue_size=10)

    start_record_srv(TriggerRequest())
    # now do something we want to record
    something_interesting()
    stop_record_srv(TriggerRequest())

    rospy.loginfo('Example code has completed, please refer to README on how to replay the data')