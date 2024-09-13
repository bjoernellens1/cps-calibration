# CPS Calibration Toolbox

This allows for fast Lidar-Camera calibration and maybe more methods follow soon.

Starting point https://github.com/PJLab-ADG/SensorsCalibration

## lidar2camera calibration
We will use the automated way leveraging SAM for preprocessing the images and we feed them to "CalibAnything" from the great toolbox.

data folder: here comes your input data (images and pcd).

### 1st extract pcds and images from rosbags
A Docker is prepared for this step, as it is usually difficult to install the correct ROS version on your system.


### 2nd SAM your images
To run SAM, we prepared a Docker compose.
to run the SAM container:

```bash
docker compose run segment-anything bash
```