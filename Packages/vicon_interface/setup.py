from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'vicon_interface'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pierre',
    maintainer_email='pmorte22@student.aau.dk',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'drone_pose_pub = vicon_interface.drone_pose_publisher_old:main',
            'pose_pub = vicon_interface.pose_publisher:main',
            'tf_pub = vicon_interface.drone_tf_publisher:main'
        ],
    },
)