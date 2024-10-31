from setuptools import setup

package_name = 'lane_slidingwindow'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='per',
    maintainer_email='per@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'sliding_window = lane_slidingwindow.lane_pub:main',
        'serial = lane_slidingwindow.lane_serial_sub:main',
                ],
    },
)
