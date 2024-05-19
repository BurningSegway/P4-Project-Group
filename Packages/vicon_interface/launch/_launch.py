import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='vicon_interface',
            executable='pose_pub',
            name='pose_pub'),
        launch_ros.actions.Node(
            package='vicon_interface',
            executable='tf_pub',
            name='tf_pub'),
  ])