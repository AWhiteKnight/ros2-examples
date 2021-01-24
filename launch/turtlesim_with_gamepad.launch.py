# A launchfile to start turtlesim with connected gamepad as input device
# tested with Logitech F710 with FoxyFitzroy on Ubuntu 20.04.1
#
# logitech F710 gamepad needs to be in mode "D", mode "X" doesn't work properly

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # start joy node
        # this will publish the topic /joy
        Node(
            package='joy',
            executable='joy_node',
            parameters=[{
                'joy_config': 'xbox',
                'deadzone': 0.01,               # depends on quality of sticks
                'autorepeat_rate': 20.0,        # in Hz
            }]
        ),
        # start teleop_twist node
        # this creates from /joy a /cmd_vel which is remapped to /turtle1/cmd_vel
        # mode "D" has 6 axis (0-5) and 12 buttons (0 - 11)
        # install packages "jstest-gtk" and or "jstest" to inspect device
        # left stick: axis 0,1 and button 10
        # right stick: axis 2,3 and button 11
        # crosspad: axis 4,5 but these are physically just tri-state switches: -val, 0, +val
        Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            parameters=[{
                'require_enable_button': True,  # we need to press security button
                'enable_button': 4,             # upper left front side button is 4
                'enable_turbo_button': 5,       # upper right front side button is 5
                'axis_linear.x': 3,             # right sticks vertical axis
                #'axis_linear.y': 0,
                #'axis_linear.z': 0,
                'scale_linear.x': 1.0,
                #'scale_linear.y': 0.0,
                #'scale_linear.z': 0.0,
                'scale_linear_turbo.x': 2.5,
                #'scale_linear_turbo.y': 0.0,
                #'scale_linear_turbo.z': 0.0,
                'axis_angular.yaw': 2,
                #'axis_angular.pitch': 0,
                #'axis_angular.roll': 0,
                'scale_angular.yaw': 1.0,       # right sticks horizontal axis
                #'scale_angular.pitch': 0.0,
                #'scale_angular.roll': 0.0,
                'scale_angular_turbo.yaw': 2.5,
                #'scale_angular_turbo.pitch': 0.0,
                #'scale_angular_turbo.roll': 0.0,
            }],
            # turtle expects topic /turtle1/cmd_vel not /cmd_vel
            remappings=[
                ('/cmd_vel', '/turtle1/cmd_vel'),
            ],
        ),
        # start turtlesim node
        Node(
            package='turtlesim',
            executable='turtlesim_node',
        ),
    ])
