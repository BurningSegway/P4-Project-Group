import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TransformStamped
from drone_msgs.msg import Pos

from tf2_ros import TransformBroadcaster
import socket 
import xml.etree.ElementTree as ET
             

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('pose_tf_publisher')
        self.frame_name = "fuglen"


        self.tf_broadcaster = TransformBroadcaster(self)
        self.subscription = self.create_subscription(Pos, 'drone/pose', self.callback, 10)
        
        self.trans_x = 0.0
        self.trans_y = 0.0
        self.trans_z = 0.0

        self.rot_e1 = 0.0
        self.rot_e2 = 0.0
        self.rot_e3 = 0.0
        self.rot_e4 = 0.0

        self.get_logger().info("--- tf publisher initiated")

    def callback(self, pose: Pos):
        
        t = TransformStamped()

        # Read message content and assign it to
        # corresponding tf variables    
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = self.frame_name

        #assing translation
        t.transform.translation.x = pose.x
        t.transform.translation.y = pose.y
        t.transform.translation.z = pose.z

        #assign rotation in quaternions
        t.transform.rotation.x = pose.e1
        t.transform.rotation.y = pose.e2
        t.transform.rotation.z = pose.e3
        t.transform.rotation.w = pose.e4

        print(t)

        # Send the transformation
        self.tf_broadcaster.sendTransform(t)


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