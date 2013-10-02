#!/usr/bin/env python

import rospy
import roslib
roslib.load_manifest("jsk_pcl_ros")
import sys
from image_view2.msg import ImageMarker2, PointArrayStamped
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA
import math

def usage():
  print "Usage: ", sys.argv[0], "id frame_id diameter [r, g, b]"
  
pub = None
def callback():
  now = rospy.Time.now()
  marker = ImageMarker2()
  marker.id = marker_id
  marker.header.frame_id = frame_id
  marker.header.stamp = now
  #marker.type = ImageMarker2.LINE_STRIP3D
  marker.type = ImageMarker2.POLYGON3D
  RESOLUTION = 20
  point_array = PointArrayStamped()
  point_array.header.frame_id = frame_id
  point_array.header.stamp = now
  for i in range(RESOLUTION + 1) + [0]:
    # x = cos(theta), y = sin(theta)
    theta = 2 * math.pi / RESOLUTION * i
    x = diameter * math.cos(theta)
    y = diameter * math.sin(theta)
    point = Point()
    point.x = x
    point.y = y
    point.z = 0
    point_array.points.append(point)
  marker.points3D = point_array
  if use_color:
    marker.outline_colors = [color]
    marker.filled = 1
    marker.fill_color = color
  pub.publish(marker)
  
def main():
  global pub, marker_id, frame_id, diameter, use_color, color
  rospy.init_node("draw_3d_circle")
  if len(rospy.myargv()) != 4 and len(rospy.myargv()) != 7:
    usage()
    exit(1)
  marker_id = int(rospy.myargv()[1])
  frame_id = rospy.myargv()[2]
  diameter = float(rospy.myargv()[3])
  pub = rospy.Publisher("image_marker", ImageMarker2)
  # loading module
  use_color = False
  color = ColorRGBA()
  if len(rospy.myargv()) == 7:
    use_color = True
    color.r = float(rospy.myargv()[4])
    color.g = float(rospy.myargv()[5])
    color.b = float(rospy.myargv()[6])
    color.a = 1.0
  while not rospy.is_shutdown():
    callback()
    rospy.sleep(1.0)
  
if __name__ == '__main__':
  try:
    main()
  except rospy.ROSInterruptException:
    pass
