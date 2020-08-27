# Simulate simple differential wheeled robot with ROS
This project was created during my studies in a purpose of simulation tool for robotic project. It was developped with **ROS melodic** version.
*This tutorial is intended for new ROS users or for developpers who wants to simulate a simple differential wheeled robot*
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

### The Part descriptor : Links
Parts are described within `link` tags.

You need to create the base of the robot. In this case its name is **base_link**. Give it a visual, collision and inertial description. Usually it's a `box` part.

><ins>Visual</ins> : What you see in the simulator.
<ins>Collision</ins> : It is used for collisions and contacts calculation in the simulator.
<ins>Inertial</ins> : How the part behaves when you add movements.

Now we can add wheels (`cylinder` part) and contacts (`sphere` part) for stabilizing the robot.

### How to describe the mechanical behavior ?

All these links have to be connected together with mecanical links. We also have to describe how parts behave together. Here comes `joint` tags.

Wheel joints have continuous type. It enable a full rotation on the `axis` (check axis tag in joint description).

>Types:
>-   <ins>revolute</ins> - a hinge joint that rotates along the axis and has a limited range specified by the upper and lower limits.
>-   <ins>continuous</ins> - a continuous hinge joint that rotates around the axis and has no upper and lower limits.
>-   <ins>prismatic</ins> - a sliding joint that slides along the axis, and has a limited range specified by the upper and lower limits.
>-   <ins>fixed</ins> - This is not really a joint because it cannot move. All degrees of freedom are locked. This type of joint does not require the axis, calibration, dynamics, limits or safety_controller.
>-   <ins>floating</ins> - This joint allows motion for all 6 degrees of freedom.
>-   <ins>planar</ins> - This joint allows motion in a plane perpendicular to the axis.

The mechanical link referential is the `parent` referential. The child corresponds to the second part of the mechanical link.

The `origin` tag corresponds to the origin of the mechanical link referential.

### My descriptor file is pretty but where is my Robot ?

ROS contains a tons of tools to simulate and visualize robots.

Here we use **Rviz** to check that the robot descriptor is correct and that the robot looks like what you want.

I advise to parse the xacro file before launching rviz.
