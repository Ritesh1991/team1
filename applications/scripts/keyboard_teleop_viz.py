#!/usr/bin/env python

import fetch_api
import rospy
from math import sqrt
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Quaternion, Pose, Point, Vector3
from nav_msgs.msg import Odometry
from std_msgs.msg import Header, ColorRGBA

from interactive_markers.interactive_marker_server import *
from visualization_msgs.msg import *

import sys, select, termios, tty

msg = """
Control Your Fetch!
---------------------------
Moving around:
        w
   a    s    d

Space: force stop
i/k: increase/decrease only linear speed by 5 cm/s
u/j: increase/decrease only angular speed by 0.25 rads/s
anything else: stop smoothly

CTRL-C to quit
"""

moveBindings = {'w': (1, 0), 'a': (0, 1), 'd': (0, -1), 's': (-1, 0)}

speedBindings = {
    'i': (0.05, 0),
    'k': (-0.05, 0),
    'u': (0, 0.25),
    'j': (0, -0.25),
}

minimum_distance = 0.5
prev_pos = []

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


speed = .2
turn = 1


def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed, turn)

def handle_viz_input(input):
    if (input.event_type == InteractiveMarkerFeedback.BUTTON_CLICK):
        rospy.loginfo(input.marker_name + ' was clicked')

def setup_interactive_marker():
    server = InteractiveMarkerServer("simple_server")
    int_marker = InteractiveMarker(name="my_marker", description="Simple Click Control")
    int_marker.header.frame_id = "base_link"

    box_marker = Marker(type = Marker.CUBE)
    box_marker.scale.x = 0.45
    box_marker.scale.y = 0.45
    box_marker.scale.z = 0.45
    box_marker.color.r = 0.0
    box_marker.color.g = 0.5
    box_marker.color.b = 0.5
    box_marker.color.a = 1.0

    button_control = InteractiveMarkerControl()
    button_control.interaction_mode = InteractiveMarkerControl.BUTTON
    button_control.always_visible = True
    button_control.markers.append( box_marker )
    int_marker.controls.append( button_control )
    
    server.insert(int_marker, handle_viz_input)
    server.applyChanges()

def show_text_in_rviz(text, marker_publisher):
    marker = Marker(
                type=Marker.TEXT_VIEW_FACING,
                id=0,
                lifetime=rospy.Duration(1.5),
                pose=Pose(Point(0.5, 0.5, 1.45), Quaternion(0, 0, 0, 1)),
                scale=Vector3(0.06, 0.06, 0.06),
                header=Header(frame_id='base_link'),
                color=ColorRGBA(0.0, 1.0, 0.0, 0.8),
                text=text)
    marker_publisher.publish(marker)

def odom_callback(message):
    global prev_pos
    x, y = message.pose.pose.position.x, message.pose.pose.position.y
    if not prev_pos:
        prev_pos.append(Point(x, y, 0))
    elif prev_pos and sqrt((x - prev_pos[-1].x) ** 2 + (y - prev_pos[-1].y) ** 2) > minimum_distance:
        prev_pos.append(Point(x, y, 0))
        marker = Marker(
                type=Marker.LINE_STRIP,
                id=0,
                scale=Vector3(0.06, 0.06, 0.06),
                points=list(prev_pos),
                header=Header(frame_id='odom'),
                color=ColorRGBA(0.0, 1.0, 0.0, 0.8))
        marker_publisher.publish(marker)


if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('fetch_teleop_key')
    base = fetch_api.Base()
    setup_interactive_marker()
    x = 0
    th = 0
    status = 0
    count = 0
    target_speed = 0
    target_turn = 0
    control_speed = 0
    control_turn = 0
    try:
        print msg
        print vels(speed, turn)
        odom_subscriber = rospy.Subscriber('/odom', Odometry, odom_callback)
        marker_publisher = rospy.Publisher('visualization_marker', Marker)
        rospy.sleep(0.5)
        show_text_in_rviz('Test publish marker twice', marker_publisher)
        while (1):
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                th = moveBindings[key][1]
                count = 0
            elif key in speedBindings.keys():
                speed += speedBindings[key][0]
                turn += speedBindings[key][1]
                count = 0

                print vels(speed, turn)
                if (status == 14):
                    print msg
                status = (status + 1) % 15
            elif key == ' ':
                x = 0
                th = 0
                control_speed = 0
                control_turn = 0
            else:
                count = count + 1
                if count > 4:
                    x = 0
                    th = 0
                if (key == '\x03'):
                    break

            target_speed = speed * x
            target_turn = turn * th

            if target_speed > control_speed:
                control_speed = min(target_speed, control_speed + 0.02)
            elif target_speed < control_speed:
                control_speed = max(target_speed, control_speed - 0.02)
            else:
                control_speed = target_speed

            if target_turn > control_turn:
                control_turn = min(target_turn, control_turn + 0.1)
            elif target_turn < control_turn:
                control_turn = max(target_turn, control_turn - 0.1)
            else:
                control_turn = target_turn
            base.move(control_speed, control_turn)
    except Exception as e:
        rospy.logerr('{}'.format(e))
    finally:
        base.stop()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

