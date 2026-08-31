import rclpy
from rclpy.node import Node

from std_msgs.msg import UInt64


class nodeA(Node):

    def __init__(self):
        # Initialize the node named NodeA
        super().__init__('nodeA')
        # Create the publisher 
        self.publisher = self.create_publisher(
            msg_type = UInt64,
            topic = 'hurtado',
            qos_profile = 10)
        
        # Create the timer at 20Hz and register the callback 
        timer_period = 0.05  # 20 Hz interval
        self.timer = self.create_timer(timer_period, self.timer_callback)
        # Declare incremental variable
        self.k = 1
        # Declare variable for increment
        self.n = 4

    def timer_callback(self):
        # Create message of type Uint64
        msg = UInt64()
        # Add k to the msg data
        msg.data = self.k
        # Publish the msg
        self.publisher.publish(msg)
        # Increment k by n
        self.k += self.n
        


def main(args=None):
    rclpy.init(args=args)

    node_A = nodeA()

    rclpy.spin(node_A)

    node_A.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()