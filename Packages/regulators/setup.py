from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'regulators'

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
            'takeoff_pub = regulators.takeoff:main',
            'z_controller = regulators.z_controller:main',
            'yaw_controller = regulators.yaw_controller:main',
            'x_controller = regulators.x_controller:main',
            'y_controller = regulators.y_controller:main',
            'x_casc = regulators.cascade_x_controller:main',
            'y_casc = regulators.cascade_y_controller:main',
            'yaw_casc = regulators.cascade_yaw_controller:main',
        ],
    },
)
