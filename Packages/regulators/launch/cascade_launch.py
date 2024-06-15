import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='regulators',
            executable='z_controller',
            name='z_controller'),
        #launch_ros.actions.Node(
        #    package='regulators',
        #    executable='yaw_casc',
        #    name='yaw_casc'),
        launch_ros.actions.Node(
            package='regulators',
            executable='x_casc',
            name='x_casc'),
        launch_ros.actions.Node(
            package='regulators',
            executable='y_controller',
            name='y_controller'),
        launch_ros.actions.Node(
            package='regulators',
            executable='yaw_controller',
            name='yaw_controller'),
  ])