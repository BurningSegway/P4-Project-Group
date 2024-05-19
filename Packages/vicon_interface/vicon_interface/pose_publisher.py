import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TransformStamped
from drone_msgs.msg import Pos

from tf2_ros import TransformBroadcaster
import socket 
import math
import xml.etree.ElementTree as ET
             

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('pose_publisher')
        self.frame_name = "fuglen"

        self.publisher_ = self.create_publisher(Pos, 'drone/pose', 10)
        #timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        
        
        self.get_logger().info("-|- waiting on connection -|-")

        
        HOST = "192.168.1.34"
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

        self.yaw = 0.0

        self.vel_x = 0.0
        self.vel_y = 0.0
        self.vel_z = 0.0

        self.get_logger().info("--- position publisher initiated")


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
                velocity = root.find('coordinate/velocity')
                self.vel_x = float(velocity.find('vx').text)
                self.vel_y = float(velocity.find('vy').text)
                self.vel_z = float(velocity.find('vz').text)
                #print("sygt")


                t = Pos()

                #assing translation
                t.x = self.trans_x
                t.y = self.trans_y
                t.z = self.trans_z

                #assign rotation in quaternions
                t.e1 = self.rot_e1
                t.e2 = self.rot_e2
                t.e3 = self.rot_e3
                t.e4 = self.rot_e4

                t.yaw = quat_2_yaw(self.rot_e1, self.rot_e2, self.rot_e3, self.rot_e4)

                t.vel_x = self.vel_x
                t.vel_y = self.vel_y
                t.vel_z = self.vel_z

                print(t)

                # Send the transformation
                self.publisher_.publish(t)
def quat_2_yaw(x, y, z, w):
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return yaw_z # in radians

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