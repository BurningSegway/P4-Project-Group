import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64
from geometry_msgs.msg import TransformStamped

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('takeoff')
        self.publisher_ = self.create_publisher(Float64, 'drone/throttle', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.subscription = self.create_subscription(TransformStamped, 'drone/pose', self.listener_callback)
        self.drone_z = 0.0
        self.drone_z_goal = 1

    def listener_callback(self, msg):
        self.drone_z = msg.transform.translation.z/1000
        self.get_logger().info(f'Current drone height: {self.drone_z}')

    
    def timer_callback(self):

        error = self.drone_z_goal - self.drone_z

        kp = 400

        temp_val = kp * error

        control_sig = 650+temp_val

        msg = Float64()
        msg.data = float(control_sig)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()