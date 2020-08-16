#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from math import atan2
from math import sqrt


rob_x = 0.0
rob_y = 0.0
rob_theta = 0.0

def getOdom(msg):
    global rob_x
    global rob_y
    global rob_theta

    rob_x = msg.pose.pose.position.x
    rob_y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation

    (roll, pitch, rob_theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

rospy.init_node("position_controller")

sub = rospy.Subscriber("/diff_drive_2W_controller/odom", Odometry, getOdom)
pub = rospy.Publisher("/diff_drive_2W_controller/cmd_vel", Twist, queue_size = 1)

goal_pose = Point()
speed_cmd = Twist()

goal_pose.x = 0
goal_pose.y = 0

rate = rospy.Rate(5)

while not rospy.is_shutdown():
    delta_x = goal_pose.x - rob_x
    delta_y = goal_pose.y - rob_y

    dist = (delta_x*delta_x)+(delta_y*delta_y)

    print('Dist = '+ str(dist)+'\n')

    delta_rot = atan2(delta_y,delta_x)

    if sqrt(dist)<0.05:
        speed_cmd.linear.x = 0
        speed_cmd.angular.z = 0

    elif (delta_rot - rob_theta > 0.3):
        speed_cmd.linear.x = 0
        speed_cmd.angular.z = 0.3

    elif (delta_rot - rob_theta < -0.3):
        speed_cmd.linear.x = 0
        speed_cmd.angular.z = 0.3

    else:
        speed_cmd.linear.x = 0.2
        speed_cmd.angular.z = 0

    pub.publish(speed_cmd)

    rate.sleep()
