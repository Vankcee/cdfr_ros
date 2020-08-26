# Simulate simple differential wheeled robot with ROS
This project was created during my studies in a purpose of simulation tool for robotic project. It was developped with **ROS melodic** version.
*This tutorial is intended for new ROS users or for developpers who wants to simulate a simple differential wheeled robot*.
## What is ROS ?
The **R**obot **O**perating **S**ystem (ROS) is a flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.

You can find more information on the [project website](https://www.ros.org/about-ros/)

## First : Install ROS
I advise you to install the latest long term service (LTS) ROS release. You can find it on the ros project main page. 

## 	

## Create the Robot Model 
>[/src/robot2W/urdf/robot_2W.urdf.xacro](https://github.com/Vankcee/cdfr_ros/blob/master/ros_ws/src/robot_2W/urdf/robot_2W.urdf.xacro)

Usually robot models are described in urdf files. In this project I used a xacro file. This is an xml macro file. It makes the model creation easier.

You can create variables, mathematical expressions and macros within the description file. XML Tags are the same as URDF.

Parts are described within `link` tags. 

You need to create the base of the robot. In this case its name is **base_link**. Give it a visual, collision and inertial description. Usually it's a `box` part.

>- <ins>Visual</ins> : What you see in the simulator.
>- <ins>Collision</ins> : It is used for collisions and contacts calculation in the simulator.
>- <ins>Inertial</ins> : How the part behaves when you add movements. 

Now we can add wheels (`cylinder` part) and contacts (`sphere` part) for stabilizing the robot.

All these links have to be connected together with mecanical links. Here comes `joint` tags.
