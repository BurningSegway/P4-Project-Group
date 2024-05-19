import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64
from std_msgs.msg import Bool
from drone_msgs.msg import Pos
from drone_msgs.msg import Goal

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('y_controller')
        self.publisher_ = self.create_publisher(Float64, 'control_input/y', 10)
        self._subscription = self.create_subscription(Pos, 'drone/pose', self.callback, 10)
        self.kill_command = self.create_subscription(Bool, 'control_input/kill', self.kill, 10)
        self.goal_sub = self.create_subscription(Goal, 'control_input/goal', self.goal_assign, 10)
        self.integral = 0
        self.prev_err = 0
        self.y_goal = 9999

        self.get_logger().info("--- y-controller launched")

    def goal_assign(self, msg):
        self.y_goal = msg.y_goal
        self.integral = 0
        self.prev_err = 0

    def callback(self, msg):

        out = Float64()


        dt = 0.01

        y_pos = msg.y

        y_err = y_pos - self.y_goal

        #Cascade controller
        K_p = 285 #controller gains #300
        K_i = 3
        K_D = 210                  #50

        self.integral += y_err * dt



        self.integral += y_err * dt


        control_sig = (y_err * K_p) + (K_i * self.integral) + (K_D*(y_err-self.prev_err)/dt)   #Output from the second controller, which the drone recieves. Should also maybe include the term that makes the drone hover

        if control_sig > 300:
            control_sig = 300

        if control_sig < -300:
            control_sig = -300

        self.prev_err = y_err
        
        out.data = float(control_sig)

        if self.y_goal != 9999:
            self.publisher_.publish(out)
            #self.get_logger().info(f"Goal: {self.x_goal}")

            print(f'Control signal: {control_sig}\n Yaw error: {y_err}\n Yaw: {y_pos}')

    def kill(self, msg):
        if msg.data == 1:
            self.get_logger().info("Recieved command to kill y-controller")
            raise SystemExit 

def main(args=None):
    rclpy.init(args=args)

    y_controller = MinimalPublisher()

    try:
        rclpy.spin(y_controller)
    except KeyboardInterrupt:
        y_controller.destroy_node()
    except SystemExit:
        y_controller.get_logger().info("Shutting down y-controller")
        y_controller.destroy_node()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()