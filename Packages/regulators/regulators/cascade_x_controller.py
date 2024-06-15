import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64
from std_msgs.msg import Bool
from drone_msgs.msg import Pos
from drone_msgs.msg import Goal

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('x_cascade_controller')
        self.publisher_ = self.create_publisher(Float64, 'control_input/x', 10)
        self._subscription = self.create_subscription(Pos, 'drone/pose', self.callback, 10)
        self.kill_command = self.create_subscription(Bool, 'control_input/kill', self.kill, 10)
        self.goal_sub = self.create_subscription(Goal, 'control_input/goal', self.goal_assign, 10)

        self.integral = 0

        self.x_goal = 9999

        self.get_logger().info("--- x_casc_controller launched")

    def goal_assign(self, msg):
        self.x_goal = msg.x_goal
        self.integral = 0
        

    def callback(self, msg):

        out = Float64()

        dt = 0.01

        x_pos = msg.x
        x_vel = msg.vel_x

        #Cascade controller
        K_p_inner = 110 #controller gains
        K_p_outer = 1.5
        K_i_outer = 30 #husk

        

        pos_err = self.x_goal - x_pos    #positional error
        outer_sig = pos_err * K_p_outer #Output from first controller
        vel_err = outer_sig - x_vel #The error signal to the second controller

        self.integral += pos_err * dt

        inner_sig = (vel_err * K_p_inner) + (K_i_outer * self.integral)    #Output from the second controller, which the drone recieves. Should also maybe include the term that makes the drone hover

        #inner_sig = K_p_inner * vel_err + 585

        if inner_sig > 300:
            inner_sig = 300

        if inner_sig < -300:
            inner_sig = -300
        
        out.data = float(inner_sig)

        if self.x_goal != 9999:
            self.publisher_.publish(out)
            self.get_logger().info(f"Goal: {pos_err}\t integral: {inner_sig}")

            print(f'Outer control signal: {outer_sig}\n Inner control signal: {inner_sig}\n Position error: {pos_err}\n Height: {x_pos}')

    def kill(self, msg):
        if msg.data == 1:
            self.get_logger().info("Recieved command to kill x-controller")
            raise SystemExit 

def main(args=None):
    rclpy.init(args=args)

    x_cascade_controller = MinimalPublisher()

    try:
        rclpy.spin(x_cascade_controller)
    except KeyboardInterrupt:
        x_cascade_controller.destroy_node()
    except SystemExit:
        x_cascade_controller.get_logger().info("Shutting down x-controller")
        x_cascade_controller.destroy_node()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()