import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import socket 
import xml.etree.ElementTree as ET
             

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('pose_publisher')
        self.frame_name = "fuglen"

        self.publisher_ = self.create_publisher(TransformStamped, 'drone/pose', 10)
        #timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        
        
        
        
        HOST = "192.168.1.35"
        PORT = 65432

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST,PORT))
        self.s.listen()
        self.conn, self.addr = self.s.accept()

        self.trans_x = 0.0
        self.trans_y = 0.0
        self.trans_z = 0.0

        self.rot_e1 = 0.0
        self.rot_e2 = 0.0
        self.rot_e3 = 0.0
        self.rot_e4 = 0.0

        self.timer_callback()


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
                self.rot_e1 = float(rotation.find('e1').text)
                self.rot_e2 = float(rotation.find('e2').text)
                self.rot_e3 = float(rotation.find('e3').text)
                self.rot_e4 = float(rotation.find('e4').text)
                rot_bol = bool(rotation.find('condition').text)
                translation = root.find('coordinate/translation')
                self.trans_x = float(translation.find('x').text)
                self.trans_y = float(translation.find('y').text)
                self.trans_z = float(translation.find('z').text)
                trans_bol = bool(translation.find('condition').text)
                #print("sygt")


                t = TransformStamped()

                # Read message content and assign it to
                # corresponding tf variables    
                t.header.stamp = self.get_clock().now().to_msg()
                t.header.frame_id = 'world'
                t.child_frame_id = self.frame_name

                #assing translation
                t.transform.translation.x = self.trans_x/1000
                t.transform.translation.y = self.trans_y/1000
                t.transform.translation.z = self.trans_z/1000

                #assign rotation in quaternions
                t.transform.rotation.x = self.rot_e1
                t.transform.rotation.y = self.rot_e2
                t.transform.rotation.z = self.rot_e3
                t.transform.rotation.w = self.rot_e4

                # Send the transformation
                self.publisher_.publish(t)


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