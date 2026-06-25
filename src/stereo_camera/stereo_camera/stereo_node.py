import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import time


class StereoNode(Node):

    def __init__(self):
        
        self.bridge = CvBridge()

        super().__init__('stereo_node')

        self._cap = cv2.VideoCapture(2)

        self.left_image_pub = self.create_publisher(
            Image,
            'left_camera/image_raw',
            10
        )

        self.right_image_pub = self.create_publisher(
            Image,
            'right_camera/image_raw',
            10
        )
      

        self.get_logger().info(
            'Stereo Node has been started.'
        )

        self.get_logger().info(
            f'Camera opened: {self._cap.isOpened()}'
        )

        ret, frame = self._cap.read()

        if ret:

            self.get_logger().info(
                f'Frame shape: {frame.shape}'
            )

        else:

            self.get_logger().error(
                'Failed to read frame'
            )

        self.timer = self.create_timer(
        0.03,
        self.publish_images
       )
    
    def publish_images(self):
        
        start = time.time()

        ret, frame = self._cap.read()

        if not ret:
            return

        width = frame.shape[1]

        mid = width // 2

        left_frame = frame[:, :mid]

        right_frame = frame[:, mid:]

        left_frame = cv2.resize(left_frame, (640, 480))
        right_frame = cv2.resize(right_frame, (640, 480))


        left_msg = self.bridge.cv2_to_imgmsg(
            left_frame,
            encoding='bgr8'
        )

        right_msg = self.bridge.cv2_to_imgmsg(
            right_frame,
            encoding='bgr8'
        )

        self.left_image_pub.publish(left_msg)

        self.right_image_pub.publish(right_msg)

        print(
                "callback:",
                            time.time() - start
        )
    
def main(args=None):

    rclpy.init(args=args)

    node = StereoNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()