import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import socket 
import xml.etree.ElementTree as ET
             

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('pose_publisher')
        self.frame_name = "drone"
        self.publisher_ = self.create_publisher(TransformStamped, 'drone/pose', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        
        
        
        HOST = "192.168.1.34"
        PORT = 65432

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST,PORT))
        self.s.listen()
        self.conn, self.addr = self.s.accept()


    def timer_callback(self):
        with self.conn:
            print(f"connected to: {self.addr}")
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                self.conn.sendall(data)
                data = data.decode()
                root = ET.fromstring(data)
                
                name = str(root.find('name').text)
                timestamp = float(root.find('time').text)
                rotation = root.find('coordinate/rotation')
                rot_e1 = float(rotation.find('e1').text)
                rot_e2 = float(rotation.find('e2').text)
                rot_e3 = float(rotation.find('e3').text)
                rot_e4 = float(rotation.find('e4').text)
                rot_bol = bool(rotation.find('condition').text)
                translation = root.find('coordinate/translation')
                trans_x = float(translation.find('x').text)
                trans_y = float(translation.find('y').text)
                trans_z = float(translation.find('z').text)
                trans_bol = bool(translation.find('condition').text)









        t = TransformStamped()
        print(msg.transform)

        # Read message content and assign it to
        # corresponding tf variables    
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = self.frame_name

        #assing translation
        t.transform.translation.x = trans_x
        t.transform.translation.y = trans_y
        t.transform.translation.z = trans_z

        #assign rotation in quaternions
        t.transform.rotation.x = rot_e1
        t.transform.rotation.y = rot_e2
        t.transform.rotation.z = rot_e3
        t.transform.rotation.w = rot_e4

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