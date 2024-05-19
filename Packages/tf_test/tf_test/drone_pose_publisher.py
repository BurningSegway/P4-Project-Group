import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class FramePublisher(Node):

    def __init__(self):
        super().__init__('drone_pose_publisher')

        #Name of transform
        self.frame_name = "fuglen"

        #Initialize the transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        self.subscription = self.create_subscription(
            TransformStamped,
            'drone/pose',
            self.handle_drone_pose,
            1)
        self.subscription  # prevent unused variable warning

    def handle_drone_pose(self, msg):
        t = TransformStamped()
        print(msg.transform)

        # Read message content and assign it to
        # corresponding tf variables    
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = self.frame_name

        #assing translation
        t.transform.translation.x = msg.transform.translation.x
        t.transform.translation.y = msg.transform.translation.y
        t.transform.translation.z = msg.transform.translation.z

        #assign rotation in quaternions
        t.transform.rotation.x = msg.transform.rotation.x
        t.transform.rotation.y = msg.transform.rotation.y
        t.transform.rotation.z = msg.transform.rotation.z
        t.transform.rotation.w = msg.transform.rotation.w

        # Send the transformation
        self.tf_broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = FramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()