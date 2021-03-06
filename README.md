# Simulate simple differential wheeled robot with ROS
This project was created during my studies in a purpose of simulation tool for robotic project. It was developped with **ROS melodic** version.
*This tutorial is intended for new ROS users or for developpers who wants to simulate a simple differential wheeled robot*
## What is ROS ?
The **R**obot **O**perating **S**ystem (ROS) is a flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.

You can find more information on the [project website](https://www.ros.org/about-ros/)

## First : Install ROS
I advise you to install the latest long term service (LTS) ROS release. You can find it on the ros project main page.

Follow installation instruction for your operating system

## Create the Robot Model
>[/src/robot2W/urdf/robot_2W.xacro](https://github.com/Vankcee/cdfr_ros/blob/master/ros_ws/src/robot_2W/urdf/robot_2W.xacro)

Usually robot models are described in urdf files. In this project I used a xacro file. This is an xml macro file. It makes the model creation easier.

You can create variables, mathematical expressions and macros within the description file. XML Tags are the same as URDF.

### The Part descriptor : Links
Parts are described within `link` tags.

You need to create the base of the robot. In this case its name is **base_link**. Give it a visual, collision and inertial description. Usually it's a `box` part.

>- <ins>Visual</ins> : What you see in the simulator.
>- <ins>Collision</ins> : It is used for collisions and contacts calculation in the simulator.
>- <ins>Inertial</ins> : How the part behaves when you add movements.

Now we can add wheels (`cylinder` part) and contacts (`sphere` part) for stabilizing the robot.

### How to describe the mechanical behavior ?

All these links have to be connected together with mecanical links. We also have to describe how parts behave together. Here comes `joint` tags.

Wheel joints have continuous type. It enable a full rotation on the `axis` (check axis tag in joint description).

>Types:
>-   revolute - a hinge joint that rotates along the axis and has a limited range specified by the upper and lower limits.
>-   continuous - a continuous hinge joint that rotates around the axis and has no upper and lower limits.
>-   prismatic - a sliding joint that slides along the axis, and has a limited range specified by the upper and lower limits.
>-   fixed - This is not really a joint because it cannot move. All degrees of freedom are locked. This type of joint does not require the axis, calibration, dynamics, limits or safety_controller.
>-   floating - This joint allows motion for all 6 degrees of freedom.
>-   planar - This joint allows motion in a plane perpendicular to the axis.

The mechanical link referential is the `parent` referential. The child corresponds to the second part of the mechanical link.

The `origin` tag corresponds to the origin of the mechanical link referential.

### My descriptor file is pretty but where is my Robot ?

ROS contains a tons of tools to simulate and visualize robots.

Here we use **Rviz** to check that the robot descriptor is correct and that the robot looks like what you want.

I advise to parse the xacro file before launching rviz:
> \>>xacro robot_2W.xacro > parse.urdf
> \>>check_urdf parse.urdf

If there's no error it shows you the root link and childs links. Otherwise the prompt helps you to modify your xacro file in order to fix issues.

When the xacro is correct, you can run rviz. I created a launcher file for rviz. It uses an rviz config file and create a rviz node.
> [/src/robot2W/launch/display.launch](https://github.com/Vankcee/cdfr_ros/blob/master/ros_ws/src/robot_2W/launch/display.launch)

You can run the launch file as follows:
> \>>roslaunch robot_2W display.launch

### Robot VIsualiZer / RVIZ
Now that RVIZ is running you have something like that :
![RVIZ Main screen with robot](https://github.com/Vankcee/cdfr_ros/blob/master/img/RVIZ_main.jpg)

Now that you can see the robot, modify it as you wish
## Control the robot
### Controllers
We want to send a movement command to robot wheels. So we need to send a message that contains command values to wheels. To simplify integration and developpement we use a model for the differential wheeled robot. It allows us to send comprehensive commands like a velocity on x axis and a rotation on z axis.

Multiple controllers exist. We can develop our own or take an existing one. Gazebo has a differential wheeled robot model controller. We use it, it is called in the xacro description file under `gazebo` tag.

Then we must configure the controller settings
> [Controller Settings](https://github.com/Vankcee/cdfr_ros/blob/master/ros_ws/src/robot_2W/config/diff_drive_2W.yaml)

Make sure that left and right wheels attributes are correct. They refer to the link of the wheel in the description file.

### First movement try
Launch Gazebo with an empty world map.
> \>> roslaunch gazebo_ros empty_world.launch

The robot need a spawner to spawn in gazebo environnement. Check my [spawner launcher](https://github.com/Vankcee/cdfr_ros/blob/master/ros_ws/src/robot_2W/launch/spawn.launch)

Gazebo looks like this now:
![Gazebo with a robot on the middle](https://github.com/Vankcee/cdfr_ros/blob/master/img/GAZEBO_main.jpg)

Try first to controll the robot with this package : [teleop_twist_keyboard](http://wiki.ros.org/teleop_twist_keyboard)
It converts your keyboard into a controll pad. To use it, launch teleop script when your robot is in gazebo environnement. Enter commands in the terminal that runs teleop script because it catches the input of the terminal.

Normally the robot moves !!!

## Automate the robot

You can create a script now to automate the robot.
I create this [script](https://github.com/Vankcee/cdfr_ros/blob/robot_control/ros_ws/src/robot_control/controller.py) under robot_control package.

It follows a path. The path is composed of waypoints of type `Point`.
It uses a PID to enslave the movement of the robot.
