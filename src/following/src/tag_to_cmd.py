#!/usr/bin/env python
import rospy

import math
import tf2_ros
import geometry_msgs.msg
from geometry_msgs.msg import PoseStamped, Pose, PoseArray, Twist
import tf_conversions
from visualization_msgs.msg import Marker

desired_distance = 0.5
desired_horizontal = 0
desired_yaw = 0
tolerance_distance = 0.1
tolerance_horizontal = 0.1
tolerance_yaw = 0.31415/4

detected = False

def pose_cb(data):
    global pose
    global detected

    try:
        pose = data.poses[0]
        detected = True
    except:
        pose = None
        detected = False
    # print(pose)

def get_command():
    try:
        distance = pose.position.x
        horizontal = pose.position.y
    except:
        distance = desired_distance
        horizontal = desired_horizontal

    speed = 0.35

    k_dis = 0.25
    k_hor = 0.25
    k_yaw = 0.5

    dis_error = (distance-desired_distance)
    hor_error = (horizontal-desired_horizontal)

    if abs(dis_error)<tolerance_distance:
        dis_error = 0
    
    if abs(hor_error)<tolerance_horizontal:
        hor_error = 0
    
    if hor_error<0:
        rotation = -1
    else:
        rotation = 1

    print(hor_error)
    print(rotation)
    rotation_error = rotation*math.atan2(abs(hor_error),abs(dis_error))

    if abs(rotation_error)<tolerance_yaw:
        rotation_error = 0
    
    if dis_error>0:
        direction = 1
    else:
        direction = -5

    desired_l_x = -(speed+direction*k_dis*(dis_error**2+hor_error**2)**(0.5))
    desired_a_z = -k_yaw*rotation_error
    # desired_l_x = k_dis*dis_error
    # desired_l_y = k_hor*hor_error
    # desired_a_z = k_yaw*yaw_error

    if desired_a_z<-0.5:
        desired_a_z = -0.5
    elif desired_a_z>0.5:
        desired_a_z = 0.5

    if desired_l_x<-1:
        desired_l_x = -1
    elif desired_l_x>0:
        desired_l_x = 0

    if not detected:
        desired_l_x = 0
        desired_a_z = 0

    twist_msg = Twist()
    twist_msg.linear.x = desired_l_x
    twist_msg.linear.y = 0
    twist_msg.linear.z = 0
    twist_msg.angular.x = 0
    twist_msg.angular.y = 0
    twist_msg.angular.z = desired_a_z

    return twist_msg

if __name__ == '__main__':
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    ar_tag_list_sub = rospy.Subscriber('/ar_tag_pos',PoseArray,pose_cb) 
    rospy.init_node('command')

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        try:
            twist_msg = get_command()
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            twist_msg = Twist()
            twist_msg.linear.x = 0
            twist_msg.linear.y = 0
            twist_msg.linear.z = 0
            twist_msg.angular.x = 0
            twist_msg.angular.y = 0
            twist_msg.angular.z = 0
            
            continue
        
        print(twist_msg)
        pub.publish(twist_msg)

        rate.sleep()