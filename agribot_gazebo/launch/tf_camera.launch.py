import os
import launch
from launch_ros.actions import Node
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='gazebo_tf_rs',
        namespace="/agribot/gazebo",
        # Euler angles : 0, 120, -90
        arguments=['0.45','0','1.5','-0.6123724','0.6123724','-0.3535534','0.3535534','base_link', 'rs_front'],
#arguments=['0.45','0','1.5','0.707','0.0','0.0','0.707','base_link', 'rs_front'],

        output='screen',
    )
    return launch.LaunchDescription([node])
