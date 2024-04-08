import rclpy
from rclpy.node import Node
import random

from geometry_msgs.msg import TransformStamped


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('pose_publisher')
        self.frame_name = "drone"
        self.publisher_ = self.create_publisher(TransformStamped, 'drone/pose', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        self.tx = 0.0
        self.ty = 0.0
        self.tz = 0.0

        self.qx = 0.0
        self.qy = 0.0
        self.qz = 0.0
        self.qw = 0.0

    def timer_callback(self):
        msg = TransformStamped()

        # Read message content and assign it to
        # corresponding tf variables
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'world'
        msg.child_frame_id = self.frame_name

        #assing translation
        msg.transform.translation.x = float(self.tx)
        msg.transform.translation.y = float(self.ty)
        msg.transform.translation.z = float(self.tz)

        #assign rotation in quaternions
        msg.transform.rotation.x = float(self.qx)
        msg.transform.rotation.y = float(self.qy)
        msg.transform.rotation.z = float(self.qz)
        msg.transform.rotation.w = float(self.qw)

        self.tx += random.uniform(-1, 1)
        if self.tx > 1:
            self.tx = 1
        if self.tx < -1:
            self.tx = -1
        self.ty += random.uniform(-1, 1)
        if self.ty > 1:
            self.ty = 1
        if self.ty < -1:
            self.ty = -1
        self.tz += random.uniform(-1, 1)
        if self.tz > 1:
            self.tz = 1
        if self.tz < -1:
            self.tz = -1

        self.qx = random.uniform(-1, 1)
        self.qy = random.uniform(-1, 1)
        self.qz = random.uniform(-1, 1)
        self.qw = random.uniform(-1, 1)

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.transform)


def main(args=None):
    rclpy.init(args=args)

    pose_publisher = MinimalPublisher()

    rclpy.spin(pose_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pose_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()