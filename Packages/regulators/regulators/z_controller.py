import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64
from std_msgs.msg import Bool
from drone_msgs.msg import Pos

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('z_controller')
        self.publisher_ = self.create_publisher(Float64, 'control_input/z', 10)
        self._subscription = self.create_subscription(Pos, 'drone/pose', self.callback, 10)
        #self.kill_command = self.create_subscription(Bool, 'control_input/kill', self.kill, 10)

    def callback(self, msg):

        out = Float64()

        z_goal = 1

        z_pos = msg.z
        z_vel = msg.vel_z

        #Cascade controller
        K_p_inner = 302 #controller gains
        K_p_outer = 2

        pos_err = z_goal - z_pos    #positional error
        outer_sig = pos_err * K_p_outer #Output from first controller
        vel_err = outer_sig - z_vel #The error signal to the second controller
        inner_sig = vel_err * K_p_inner + 700    #Output from the second controller, which the drone recieves. Should also maybe include the term that makes the drone hover

        if inner_sig > 1000:
            inner_sig = 1000

        if inner_sig < 200:
            inner_sig = 200
        
        out.data = float(inner_sig)

        self.publisher_.publish(out)
        print(f'Outer control signal: {outer_sig}\n Inner control signal: {inner_sig}\n Position error: {pos_err}')

        #PD controller

    def kill(self, msg):
        if msg.data == 1:
            self.get_logger().info("Recieved command to kill z-controller")
            raise SystemExit 

def main(args=None):
    rclpy.init(args=args)

    z_controller = MinimalPublisher()

    try:
        rclpy.spin(z_controller)
    except KeyboardInterrupt:
        z_controller.destroy_node()
    except SystemExit:
        z_controller.get_logger().info("Shutting down z-controller")
        z_controller.destroy_node()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()