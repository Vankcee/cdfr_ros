#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from math import atan2
from math import sqrt

speed_cmd=None

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

error_value = 0
sum_error = 0
dt_error = 0

prev_error = 0
prev_time = rospy.get_time()

P = 1.5
I = 0.0001
D = 2

def pid(value,objectif):
    global error_value
    global sum_error
    global dt_error

    global prev_error
    global prev_time

    error_value = objectif - value
    sum_error = sum_error + error_value
    current_time = rospy.get_time()
    dt_time = current_time - prev_time

    if dt_time:
        dt_error = (error_value-prev_error)/(dt_time)
    else:
        dt_error = (error_value-prev_error)/(0.0001)

    prev_time = current_time
    prev_error = error_value
    cmd = (P * error_value) + (I*sum_error) + (D*dt_error)

    return cmd

rob_x = 0.0
rob_y = 0.0
rob_theta = 0.0

speed_cmd = Twist()

waypoints = []
waypoints.append( Point(2,4,0))
waypoints.append( Point(5,7,0))
waypoints.append( Point(2,-3,0))
waypoints.append( Point(-1,-1,0))

rate = rospy.Rate(10)

def calc_cmd(goal):
    cmd = Twist()

    delta_x = goal.x - rob_x
    delta_y = goal.y - rob_y
    goal_rot = atan2(delta_y,delta_x)
    dist = sqrt((delta_x*delta_x)+(delta_y*delta_y))

    if dist >= 0.2:
        cmd.linear.x = dist
        cmd.angular.z = pid(rob_theta,goal_rot)
    else:
        cmd.linear.x = 0
        cmd.angular.z = 0
    return cmd

def isNear(x,y):
    result = False

    delta_x = x - rob_x
    delta_y = y - rob_y

    dist = sqrt((delta_x*delta_x)+(delta_y*delta_y))

    if (dist<0.2):
        result = True
    return result

def follow_way():
    global speed_cmd

    if not isNear(waypoints[-1].x,waypoints[-1].y):
        for goal in waypoints:
            print("GOAL : X = "+str(goal.x)+" // Y = "+str(goal.y))
            while not isNear(goal.x,goal.y):
                speed_cmd = calc_cmd(goal)
                pub.publish(speed_cmd)
                rate.sleep()
            print("AT : X = "+str(rob_x)+" // Y = "+str(rob_y))
    speed_cmd.linear.x = 0
    speed_cmd.angular.z = 0
    pub.publish(speed_cmd)
    print("GOAL ACHIEVED !")

while not rospy.is_shutdown():
    follow_way()
