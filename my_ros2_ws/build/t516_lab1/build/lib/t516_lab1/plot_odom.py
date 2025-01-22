#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import matplotlib.pyplot as plt
import time


class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('odom_subscriber')
        self.subscription = self.create_subscription(
            Odometry,  # 消息类型
            '/odom',  # 订阅的主题
            self.odom_callback,  # 回调函数
            10  # 队列深度
        )
        self.last_time = time.time()  # 用于限制数据采样频率
        self.x_data = []  # 存储 X 位置
        self.y_data = []  # 存储 Y 位置

    def odom_callback(self, msg):
        current_time = time.time()
        # 限制每 0.1 秒采样一次
        if current_time - self.last_time < 0.1:
            return
        self.last_time = current_time

        # 获取位置数据
        position = msg.pose.pose.position
        x = position.x
        y = position.y

        # 日志输出当前位置
        self.get_logger().info(f"Position -> x: {x}, y: {y}")

        # 添加到绘图数据
        self.x_data.append(x)
        self.y_data.append(y)

    def plot_data(self):
        # 绘制机器人轨迹
        plt.figure()
        plt.plot(self.x_data, self.y_data, label='Odometry Path')
        plt.title('Odometry X-Y Path')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.legend()
        plt.grid(True)
        plt.show()


def main(args=None):
    rclpy.init(args=args)
    odom_subscriber = OdomSubscriber()

    try:
        rclpy.spin(odom_subscriber)
    except KeyboardInterrupt:
        # 程序终止时绘制轨迹
        odom_subscriber.plot_data()

    odom_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

