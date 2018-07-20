# Data Recording
This is a simple ROS package that allows starting and stopping rosbag recordings via service calls, 
which is useful for performing repeated data collection. It also allows replaying those recordings for
analyzing performance.

## Run
`roslaunch data_recording data_recording.launch` uses the default mode:=minimal.  

## Config
The config files for the recording are in the config directory. You can choose between different settings and add new config files.
Configure the output directory for the rosbag files and topics to be recorded (regex syntax is ok).
Rosbag files are saved with the current date and time as a filename.

## Usage

The package creates three services, which can be called with a `std_srvs.srv.TriggerRequest` message:
* /data\_recording/start\_recording
* /data\_recording/stop\_recording
* /data\_recording/toggle\_recording

Add the following import to your ROS node:

`from std_srvs.srv import Trigger`

In the init of your ROS node, launch the services as
```python
start_record_srv = rospy.ServiceProxy('/data_recording/start_recording', Trigger)
stop_record_srv = rospy.ServiceProxy('/data_recording/stop_recording', Trigger)
```

Then in a regular service call:

```python
start_record_srv(TriggerRequest())
do_some_stuff()
stop_record_srv(TriggerRequest())
```

### Annotations

From within the code you can add annotations to the stored rosbags by publishing 
strings to a special topic `/data_recording/annotations`. 
Simply create a publisher in your initialization: 
```python
annotation_pub = rospy.Publisher('/data_recording/annotations', Marker, queue_size=10)
```
and add `from visualization_msgs.msg import Marker` to your imports.

Then create a text marker:

```python
text_marker = Marker()
text_marker.header.stamp = rospy.get_rostime()
text_marker.header.frame_id = "/world" # You can also put text on say the end effector!
text_marker.type = 9  # this specifies that the marker is a text marker
text_marker.pose.position = {x: 0.0, y: 0.0, z: 0.0}
text_marker.pose.orientation = {x: 0.0, y: 0.0, z: 0.0, w: 0.0}
text_marker.scale = {x: 0.5, y: 0.5, z: 0.5} # units?
text_marker.color = {r: 1.0, g: 0.0, b: 0.0, a: 1.0} # make sure 'a' is set to >0, otherwise invisible
text_marker.lifetime = {secs: 2, nsecs: 0}
text_marker.text = "Your message here"
```

You probably want to wrap this in a utils method that you can import.

Publish an annotation any time anywhere using `annotation_pub.publish(text_marker)`

## Replaying a rosbag

Kill all ROS nodes currently running. This file will launch all necessary nodes and rviz for you.

```roslaunch data_recording replay.launch filename:=YOUR_RECORDING```

This launch file assumes a specific path for the recordings which you can
specify using `filepath:=YOUR_FILEPATH`.

This launch file launches a specific rviz config file. You can make a new file, store it in the config folder
and load it using the `mode` argument.

