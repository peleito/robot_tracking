# robot_tracking

Build, source, and run code
```
cd ~/robot_tracking
catkin_make
source devel/setup.bash
roslaunch following follow.launch
```
Set up launch file to run on computer start up
```
rosrun robot_upstart install following/launch/follow.launch --job robot_following_ros --symlink
```
Start launch service
```
sudo systemctl start robot_following_ros.service
```
Stop launch service
```
sudo systemctl stop robot_following_ros.service
```
Disable launch service from starting on computer start up
```
sudo systemctl disable robot_following_ros.service
```
Remove service completely from computer
```
rosrun robot_upstart uninstall robot_following_ros
```

References for running launch file on startup: https://roboticsbackend.com/make-ros-launch-start-on-boot-with-robot_upstart/
