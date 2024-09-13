import os
import rosbag
import cv2
from cv_bridge import CvBridge
import numpy as np
import sensor_msgs.point_cloud2 as pc2
import yaml
import argparse

# Initialize CvBridge
bridge = CvBridge()

def save_camera_info(camera_info, output_folder):
    camera_info_dict = {
        "K": camera_info.K,
        "D": camera_info.D,
        "R": camera_info.R,
        "P": camera_info.P,
        "distortion_model": camera_info.distortion_model,
    }
    with open(os.path.join(output_folder, 'camera_info.yaml'), 'w') as file:
        yaml.dump(camera_info_dict, file)

def extract_rosbag_data(bag_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    bag = rosbag.Bag(bag_file, 'r')
    for topic, msg, t in bag.read_messages(topics=['/camera/color/image_raw', '/ouster/points', '/camera/color/camera_info']):
        timestamp = str(t.to_nsec())
        if topic == '/camera/color/image_raw':
            # Convert ROS Image message to OpenCV image
            cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            image_filename = os.path.join(output_folder, f'{timestamp}.png')
            cv2.imwrite(image_filename, cv_image)
        elif topic == '/ouster/points':
            # Convert PointCloud2 message to array and save to a .pcd file
            points = []
            for point in pc2.read_points(msg, field_names=("x", "y", "z", "intensity"), skip_nans=True):
                points.append([point[0], point[1], point[2], point[3]])
            points_array = np.array(points)
            pcd_filename = os.path.join(output_folder, f'{timestamp}.pcd')
            with open(pcd_filename, 'w') as pcd_file:
                pcd_file.write('# .PCD v0.7 - Point Cloud Data file format\n')
                pcd_file.write('FIELDS x y z intensity\n')
                pcd_file.write('SIZE 4 4 4 4\n')
                pcd_file.write('TYPE F F F F\n')
                pcd_file.write('COUNT 1 1 1 1\n')
                pcd_file.write(f'WIDTH {len(points_array)}\n')
                pcd_file.write('HEIGHT 1\n')
                pcd_file.write('VIEWPOINT 0 0 0 1 0 0 0\n')
                pcd_file.write(f'POINTS {len(points_array)}\n')
                pcd_file.write('DATA ascii\n')
                np.savetxt(pcd_file, points_array, fmt='%.8f %.8f %.8f %.8f')

        elif topic == '/camera/color/camera_info':
            # Save camera intrinsics
            save_camera_info(msg, output_folder)

    bag.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract data from a ROS bag file.')
    parser.add_argument('bag_file', type=str, help='Path to the ROS bag file')
    parser.add_argument('output_folder', type=str, help='Directory where the output files will be saved')

    args = parser.parse_args()

    extract_rosbag_data(args.bag_file, args.output_folder)
