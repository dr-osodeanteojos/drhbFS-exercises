import rclpy
from rclpy.node import Node

from std_msgs.msg import UInt64, Float64

class nodeB(Node):

    def __init__(self):
        # Initialize the node named NodeB
        super().__init__('nodeB')
        # Create a subscription to the 'hurtado' topic
        self.hurtado_subscription = self.create_subscription(
            msg_type = UInt64,
            topic = 'hurtado',
            callback = self.listener_callback,
            qos_profile = 10)
        self.hurtado_subscription
        # Declare the q value
        self.q = 0.15

        # Create the publisher for the result
        self.result_publisher = self.create_publisher(
            msg_type = Float64,
            topic = 'kthfs/result',
            qos_profile = 10)
                

    def listener_callback(self, msg):
        incoming_number = msg.data
        result = incoming_number/self.q
        #self.get_logger().info('Result is %f' %result)
        # Create message of type Float64
        result_msg = Float64()
        # Add result to the msg data
        result_msg.data = result
        # Publish the msg
        self.result_publisher.publish(result_msg)

        
        


def main(args=None):
    rclpy.init(args=args)

    node_B = nodeB()

    rclpy.spin(node_B)

    node_B.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()