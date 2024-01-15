from setuptools import setup

package_name = 'lane_hough'

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
        'hough = lane_hough.lane_check:main',
        'serial = lane_hough.lane_serial:main',
        'scan = lane_hough.lane_scan:main',
        'scan30 = lane_hough.lane_scan_30:main',
        
        ],
    },
)
