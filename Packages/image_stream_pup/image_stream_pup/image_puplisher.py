# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError
import numpy as np


from std_msgs.msg import Bool
from sensor_msgs.msg import Image


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('image_pupblisher')
        self.publisher_ = self.create_publisher(Image, 'camera/image', 1)
        self.command_sub = self.create_subscription(Bool, 'camera/command', self.capture, 10)

        self.bridge = CvBridge()

        cam_port = 1
        self.cam = cv.VideoCapture(cam_port)
        result, image = self.cam.read()

        if result:
            self.get_logger().info("Camera initialized!")
        else:
            self.get_logger().info("Camera not initialized!")

    def capture(self, msg):

        if self.cam.isOpened() and msg.data == 1:
            _, image = self.cam.read()

            #Lav billede om til sensor_msg Image
            i = Image()
            i.header.stamp = Node.get_clock(self).now().to_msg()
            i.header.frame_id = "Webcam"
            i.height = np.shape(image)[0]
            i.width = np.shape(image)[1]
            i.encoding = "bgr8"
            i.is_bigendian = False
            i.step = np.shape(image)[2] * np.shape(image)[1]
            i.data = np.array(image).tobytes()

            #Publish billede
            self.publisher_.publish(i)
            self.get_logger().info("Image pupblished")



def main(args=None):
    rclpy.init(args=args)

    image_pupblisher = MinimalPublisher()

    rclpy.spin(image_pupblisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    image_pupblisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
