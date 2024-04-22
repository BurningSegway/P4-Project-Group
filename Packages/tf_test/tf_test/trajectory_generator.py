import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TransformStamped

import math as m
import numpy as np

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('traj_publisher')
        self.frame_name = "drone"
        self.publisher_ = self.create_publisher(TransformStamped, 'drone/pose', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        self.trans_start = [0, 0, 0]
        self.trans_finish = [1, -0.75, 0.50]

        self.rot_start = 0

        self.rot_finish = 0

        #Avg. speed
        self.v = 0.1

        #Calc. distance
        self.d = m.sqrt(m.pow((self.trans_finish[0]-self.trans_start[0]),2)+m.pow((self.trans_finish[1]-self.trans_start[1]),2)+m.pow((self.trans_finish[2]-self.trans_start[2]),2))

        #Calc. the time it takes to finish
        self.tf = self.d/self.v

        #Number of steps in tf given frequency
        self.n = int(self.tf / timer_period)
        #Size or time in each segemnt of the interval
        self.dt = self.tf/self.n

        self.time_step = timer_period/self.tf
        print(f"Time step*: {self.time_step}")

        #Calc. constants
        self.a0 = [
            self.trans_start[0],
            self.trans_start[1],
            self.trans_start[2]]

        self.a1 = [
            0, 
            0, 
            0]

        self.a2 = [
            (3/m.pow(self.tf,2))*(self.trans_finish[0]-self.trans_start[0]), 
            (3/m.pow(self.tf,2))*(self.trans_finish[1]-self.trans_start[1]), 
            (3/m.pow(self.tf,2))*(self.trans_finish[2]-self.trans_start[2])]

        self.a3 = [
            -(2/m.pow(self.tf,3))*(self.trans_finish[0]-self.trans_start[0]),
            -(2/m.pow(self.tf,3))*(self.trans_finish[1]-self.trans_start[1]),
            -(2/m.pow(self.tf,3))*(self.trans_finish[2]-self.trans_start[2])]
        
        print(self.a2)
        print(self.a3)
        
    def timer_callback(self):
        tau = self.i * self.dt

        if tau > self.tf:
            tau = self.tf
            raise SystemExit

        msg = TransformStamped()

        # Read message content and assign it to
        # corresponding tf variables
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'world'
        msg.child_frame_id = 'drone'

        #assing translation
        msg.transform.translation.x = float(self.a0[0] + self.a1[0]*tau + self.a2[0]*m.pow(tau,2) + self.a3[0]*m.pow(tau, 3))
        msg.transform.translation.y = float(self.a0[1] + self.a1[1]*tau + self.a2[1]*m.pow(tau,2) + self.a3[1]*m.pow(tau, 3))
        msg.transform.translation.z = float(self.a0[2] + self.a1[2]*tau + self.a2[2]*m.pow(tau,2) + self.a3[2]*m.pow(tau, 3))

        #assign rotation in quaternions
        msg.transform.rotation.x = 0.0
        msg.transform.rotation.y = 0.0
        msg.transform.rotation.z = 0.0
        msg.transform.rotation.w = 1.0

        self.publisher_.publish(msg)
        self.get_logger().info(f'\n Speed: {self.v}\n Distance: {self.d}\n Time: {self.tf}\n Elapsed time: {tau}\n -\n X: {msg.transform.translation.x}\n Y: {msg.transform.translation.y}\n Z: {msg.transform.translation.z}\n ---')
       

        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    traj_publisher = MinimalPublisher()

    try:
        rclpy.spin(traj_publisher)
    except SystemExit:
        rclpy.logging.get_logger("INFO").info("Goal reached, quitting...")

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    traj_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()