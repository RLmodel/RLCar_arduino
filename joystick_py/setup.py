from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'joystick_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='per',
    maintainer_email='ojh2079@rlmodel.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            #'joy_test=joystick_py.joy_node:main',
            #'joy_to_cmd=joystick_py.joy_KSY:main',
            'joy_0709=joystick_py.joy_0709:main',
        ],
    },
)
