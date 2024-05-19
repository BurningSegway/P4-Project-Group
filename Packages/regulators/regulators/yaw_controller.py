import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64
from std_msgs.msg import Bool
from drone_msgs.msg import Pos

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('yaw_controller')
        self.publisher_ = self.create_publisher(Float64, 'control_input/yaw', 10)
        self._subscription = self.create_subscription(Pos, 'drone/pose', self.callback, 10)
        self.kill_command = self.create_subscription(Bool, 'control_input/kill', self.kill, 10)
        self.integral = 0
        self.prev_err = 0

        self.get_logger().info("--- yaw-controller launched")

    def callback(self, msg):

        out = Float64()

        yaw_goal = 0

        dt = 0.01

        yaw_pos = msg.yaw

        yaw_err = yaw_pos - yaw_goal

        #Cascade controller
        K_p = 8 #controller gains
        K_i = 2
        K_D = 3



        self.integral += yaw_err * dt


        control_sig = (yaw_err * K_p) + (K_i * self.integral) + (K_D*(yaw_err-self.prev_err)/dt)   #Output from the second controller, which the drone recieves. Should also maybe include the term that makes the drone hover

        if control_sig > 300:
            control_sig = 300

        if control_sig < -300:
            control_sig = -300

        
        out.data = float(control_sig)

        self.publisher_.publish(out)
        print(f'Control signal: {control_sig}\n Yaw error: {yaw_err}\n Yaw: {yaw_pos}')

    def kill(self, msg):
        if msg.data == 1:
            self.get_logger().info("Recieved command to kill yaw-controller")
            raise SystemExit 

def main(args=None):
    rclpy.init(args=args)

    yaw_controller = MinimalPublisher()

    try:
        rclpy.spin(yaw_controller)
    except KeyboardInterrupt:
        yaw_controller.destroy_node()
    except SystemExit:
        yaw_controller.get_logger().info("Shutting down yaw-controller")
        yaw_controller.destroy_node()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()