import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64
from std_msgs.msg import Bool
from drone_msgs.msg import Pos
from drone_msgs.msg import Goal

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('yaw_cascade_controller')
        self.publisher_ = self.create_publisher(Float64, 'control_input/yaw', 10)
        self._subscription = self.create_subscription(Pos, 'drone/pose', self.callback, 10)
        self.kill_command = self.create_subscription(Bool, 'control_input/kill', self.kill, 10)

        self.integral = 0

        self.get_logger().info("--- yaw_casc_controller launched")        

    def callback(self, msg):

        out = Float64()

        dt = 0.01

        yaw_goal = 0

        yaw_pos = msg.yaw
        yaw_vel = msg.yaw_vel

        #Cascade controller
        K_p_inner = 50 #controller gains
        K_p_outer = 1.3
        K_i_outer = 35 #husk

        

        pos_err = yaw_pos - yaw_goal    #positional error
        outer_sig = pos_err * K_p_outer #Output from first controller
        vel_err = outer_sig - yaw_vel #The error signal to the second controller

        self.integral += pos_err * dt

        inner_sig = (vel_err * K_p_inner) + (K_i_outer * self.integral)    #Output from the second controller, which the drone recieves. Should also maybe include the term that makes the drone hover

        #inner_sig = K_p_inner * vel_err + 585

        if inner_sig > 300:
            inner_sig = 300

        if inner_sig < -300:
            inner_sig = -300
        
        out.data = float(inner_sig)

        self.publisher_.publish(out)
        self.get_logger().info(f"Goal: {pos_err}\t integral: {inner_sig}")

        print(f'Outer control signal: {outer_sig}\n Inner control signal: {inner_sig}\n Position error: {pos_err}\n Height: {yaw_pos}')

    def kill(self, msg):
        if msg.data == 1:
            self.get_logger().info("Recieved command to kill yaw-controller")
            raise SystemExit 

def main(args=None):
    rclpy.init(args=args)

    yaw_cascade_controller = MinimalPublisher()

    try:
        rclpy.spin(yaw_cascade_controller)
    except KeyboardInterrupt:
        yaw_cascade_controller.destroy_node()
    except SystemExit:
        yaw_cascade_controller.get_logger().info("Shutting down yaw-controller")
        yaw_cascade_controller.destroy_node()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()