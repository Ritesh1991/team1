#!/usr/bin/env python

import pickle
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped

POSE_FILE = 'poses'
SUB_NAME = 'amcl_pose'
PUB_NAME = 'move_base_simple/goal'

class PoseController(object):
    def __init__(self):
        self._pose_sub = rospy.Subscriber(SUB_NAME,
                                          PoseWithCovarianceStamped, 
                                          callback=self._pose_callback)
        self._pose_pub = rospy.Publisher(PUB_NAME,
                                         PoseStamped,
                                         queue_size=10)
        self._poses = self._read_in_poses()
        self._curr_pose = None

    def __str__(self):
        if self._poses:
            return "Poses:\n" "\n".join(["{}:\n{}".format(name, pose) for name, pose in self._poses.items()])
        else:
            return "No poses"

    def _read_in_poses(self):
        try:
            with open(POSE_FILE, 'rb') as file:
                return pickle.load(file)
        except IOError:
            return {}

    def _write_out_poses(self):
        with open(POSE_FILE, 'wb') as file:
            pickle.dump(self._poses, file)

    def _pose_callback(self, msg):
        self._curr_pose = msg

    def save_pose(self, pose_name):
        if not self._curr_pose:
            print "No pose available"
            return
        print "Saving pose {} as current position".format(pose_name)
        self._poses[pose_name] = self._curr_pose
        self._write_out_poses()

    def delete_pose(self, pose_name):
        if pose_name in self._poses:
            del self._poses[pose_name]
            print "Pose {} deleted".format(pose_name)
            self._write_out_poses()
        else:
            print "Pose name {} does not exist".format(pose_name)

    def rename_pose(self, pose_name, pose_name_new):
        if pose_name in self._poses:
            self._poses[pose_name_new] = self._poses[pose_name]
            del self._poses[pose_name]
            print "Pose {} renamed to {}".format(pose_name, pose_name_new)
            self._write_out_poses()
        else:
            print "Pose name {} does not exist".format(pose_name)

    def edit_pose(self, pose_name, pose):
        if pose_name in self._poses:
            self._poses[pose_name] = pose
            self._write_out_poses()

    @property
    def poses(self):
        return self._poses

    @property
    def curr_pose(self):
        return self._curr_pose

    def move_to_pose(self, pose_name):
        if pose_name in self._poses:
            msg = PoseStamped()
            msg.header = self._poses[pose_name].header
            msg.pose = self._poses[pose_name].pose.pose
            self._pose_pub.publish(msg)

