## Launching map annotator RViz web interface:

1. `roscore`
2. `gazebo`
3. `rviz`
4. `backendrviz`
5. RViz: in the InteractiveMarkers -> Update Topic dropdown, select '/simple_server/update'
6. `frontendrviz`
7. Visit http://localhost:8080/ and use the Websocket URL: ws://localhost:9090

Navigation Docs-for running robot in real life
===============

This README guides you through the map building process in the real world using Astro.

In a tmux terminal, run the following commands...
---
To run the exisitng map file and save poses do this:
####In one terminal:
```
ssh team1@astro
```
Launch the fetch navigation: fetch_nav with map file real_robot_take_1.yaml and keepout obstacles_small_room.yaml: change if you need
```
roslaunch map_annotator navigation.launch
```
####Then run in another terminal:
```
ssh team1@astro
```
```
roslaunch fetch_api move_group.launch
```

####In another terminal:
```
setrobot astro
```
```
rosrun rviz rviz -d ~/catkin_ws/src/cse481c/applications/config/navigation.rviz
```

---
To build map in the real world, run the following commands (in tmux if you want to keep your sanity)...

STEP 1: Breathe.  <br />
STEP 2: 'setrobot astro'  <br />
[ONLY DO IF NEED TO CONFIG RVIZ] STEP 3: `roslaunch fetch_navigation build_map.launch`  <br />
[ONLY DO IF NEED TO CONFIG RVIZ] STEP 4: `rosrun rviz rviz`  <br />
[ONLY DO IF NEED TO CONFIG RVIZ] STEP 5: Make sure the Rviz configuration has all the views specified in Lab 16.  <br />
* Robot model
* Grid
* Map
* Laser scan
* Image
* Fixed frame = map  <br />

[ONLY DO IF NEED TO CONFIG RVIZ] STEP 6: shutdown rviz and build_map.launch  <br />
STEP 7: `roslaunch applications build_map_real.launch`  <br />
STEP 8: NOW, drive the robot around to bulid a map of the world! How excite.  <br />
STEP 9: Happy with your map? Now run `rosrun map_server map_saver -f ~/maps/your_name_of_map_file_here`  <br />
STEP 10: DONEZO  <br />



---

To build map in simulation, run the following commands (in tmux if you want to keep your sanity)...

STEP 1: `roscore` <br />
STEP 2: `gazebo` <br />
[ONLY DO IF NEED TO CONFIG RVIZ] STEP 3: `roslaunch fetch_navigation build_map.launch`  <br />
[ONLY DO IF NEED TO CONFIG RVIZ] STEP 4: `rosrun rviz rviz`  <br />
[ONLY DO IF NEED TO CONFIG RVIZ] STEP 5: Make sure the Rviz configuration has all the views specified in Lab 16.  <br />
* Robot model
* Grid
* Map
* Laser scan
* Image
* Fixed frame = map  <br />

[ONLY DO IF NEED TO CONFIG RVIZ] STEP 6: shutdown rviz and build_map.launch  <br />
STEP 7: `roslaunch applications build_map.launch`  <br />
STEP 8: NOW, drive the robot around to bulid a map of the world! How excite.  <br />
STEP 9: Happy with your map? Now run `rosrun map_server map_saver -f ~/maps/your_name_of_map_file_here`  <br />
STEP 10: DONEZO  <br />


---

*Make sure everything is set to astro before running!*

```
setrobot astro
```
```
roslaunch fetch_navigation build_map.launch
```

---

Now, teleoperate the robot around.
```
rosrun rviz rviz
```
From here, open the `map_creator.rviz` config file in RViz.

---

* Once happy with map created by driving the robot, save the map:
```
rosrun map_server map_saver -f maps/map_name
```

