#!/usr/bin/env python
# from traceback import print_tb
# from rospy.names import reload_mappings
import rospy 
from geometry_msgs.msg import Pose, PoseArray 
from ar_track_alvar_msgs.msg import AlvarMarkers

class ar_tag():
    def __init__(self):
        self.ar_tag_pos_pub = rospy.Publisher('/ar_tag_pos',PoseArray,queue_size=100)
        self.ar_tag_list_sub = rospy.Subscriber('/ar_pose_marker',AlvarMarkers,self.__ar_tags_list_cb) 
        self.num_markers = 0
        self.marker_info = None

    def ar_pos_pub(self):
        poses = []
        marker_msg = Pose()
        msg = PoseArray()
        for i in range(self.num_markers):
            print(type(self.marker_info.markers[i].id))
            marker_msg.position = self.marker_info.markers[i].pose.pose.position
            marker_msg.orientation = self.marker_info.markers[i].pose.pose.orientation
            poses.append(marker_msg)    
        msg.poses = poses
        self.ar_tag_pos_pub.publish(msg)


    def __ar_tags_list_cb(self,data):
        self.num_markers = len(data.markers)
        self.marker_info = data
        # print(self.marker_info)
        
        

if __name__ == '__main__':
    rospy.init_node('ar_tag_pose')

    current_ar_tags = ar_tag()

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        current_ar_tags.ar_pos_pub()
        print('Number of labels: ',current_ar_tags.num_markers)
        rate.sleep()