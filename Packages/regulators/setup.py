from setuptools import find_packages, setup

package_name = 'regulators'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'z_controller = regulators.z_controller:main'
        ],
    },
)
