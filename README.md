# CSE 481C
[View the Nectar team blog here](https://cse481team1.tumblr.com/)

## Maaja Nectar Website
Dependencies:
* apt-get install npm
* npm install bower -g
* npm install gulp -g

To serve, run the following commands:
1. In one bash window, run the backend server:
```
python server.py
```
2. In a second bash window, server the frontend:
```
npm install && npm update
bower install && bower update

# single-client
cd web_nectar && gulp serve

# multi-client
cd web_nectar && python -m SimpleHTTPServer 3000
```
## Nectar Backend
1. ssh into the robot
2. `roslaunch backend_nectar nectar.launch`
3. If you want rviz, then open rviz on your computer with some config

## Launching web interface:
1. `roscore`
2. `gazebo`
3. `frontend`
4. `backend`
5. Visit http://localhost:8080/ and use the Websocket URL: ws://localhost:9090

## ROS dependencies
sudo apt-get install ros-indigo-simple-grasping

