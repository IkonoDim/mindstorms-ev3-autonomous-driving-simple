# Robot Control System with Sensor Data Streaming
## Project Overview
This project involves the development of a robot control system using the Pybricks Micropython framework on an EV3 
brick. The system includes components for motor control, gyro sensor-based orientation stabilization, and sensor data 
streaming over a network socket. The project is divided into two main scripts: one for controlling the robot and another
for simulating a server that streams sensor data to the robot.

3 Modules of the Mindstorms Brick were used. (red set)
- 2x Large Motor (6009430) in port A and port D
- 1x Gyro Sensor (6008916) in port 4

Authors: Dimitrios Ikonomou, Nue Duhanaj

![python](https://img.shields.io/badge/MicroPython-14354C?style=for-the-badge&logo=python&logoColor=white) 
![pycharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)

--- 
## Script 1: Robot Control System
### Description
The first application is responsible for controlling the robot's movement and stabilization. It uses motors for movement
and a gyro sensor to maintain orientation. The script also includes functionality to connect to a sensor-server and 
receive sensor data, which informs the robot's actions.
### Key Components
#### Imports and Initialization
- **Imports**: The script imports necessary modules including time, _thread, socket, and Pybricks components.
- **Initialization**: Initializes the EV3 brick, motors, and gyro sensor.
#### Globals Class
- **Globals**: Defines a class to store global variables such as the sensor server host, turning status, sensor data, 
and stabilization angle.
#### Motor Control Functions
- **`start_both_motors(speed: int) -> None`:** Starts both motors at the given speed.
- **`stop_both_motors(hold: bool = False) -> None`:** Stops both motors, optionally holding their position.
- **`set_speed_both_motors(speed: int)`:** Sets the speed of both motors.
- **`turn(speed: int, angle: int) -> None`:** Turns the robot to a specific angle.
#### Sensor Data Streaming
- **`stream_sensor_data() -> None`:** Establishes a socket connection to stream sensor data and updates the global 
sensor data.
#### Main Algorithm
- **`algorithm()`:** Main algorithm that decides robot actions based on sensor data.

<img src="https://github.com/IkonoDim/mindstorms-ev3-autonomous-driving-simple/blob/main/assets/structogram_core.png?raw=true" width="100%" alt="">\
When navigating, the robot follows a set of predefined rules to maneuver around obstacles and stabilize its course. 
Here's how it operates:\
If the front is blocked and the left side is clear, the robot will turn left. Conversely, if the front is blocked and 
the right side is clear, it will turn right. When all three directions—the front, left, and right—are blocked, the robot 
moves backward until either the left or right becomes free, at which point it turns in the corresponding direction.
In cases where only the front and right are blocked, the robot will turn left. If only the front and left are blocked, 
it will turn right.\
Additionally, the robot continuously monitors its stabilization angle. If the angle is positive, indicating a deviation 
that needs correction, the robot will turn to stabilize its course. Similarly, if the stabilization angle is negative, 
it will turn to correct the course deviation.\
Through this systematic approach, the robot effectively navigates its environment while maintaining stability.

#### Direction stabilization Algorithm
- **`stabilize_motors() -> None`:** Continuously adjusts the robot's orientation to maintain stability.

<img src="https://github.com/IkonoDim/mindstorms-ev3-autonomous-driving-simple/blob/main/assets/structogram_stabilization.png?raw=true" width="65%" alt="">


#### Main Function
- **`main()`:** Starts the robot control script, initializes motor control and sensor data streaming threads, and runs 
the main algorithm.

---
## Script 2: Sensor Data Streaming Server
### Description
The second application functions as a server that streams real-time sensor data to the robot over a network 
socket. It establishes socket communication to transmit actual sensor data updates and heartbeat signals at regular 
intervals. The script reads sensor data from specified IO pins or hardware inputs, depending on whether it runs on 
MicroPython or another python environment.\
Sensors used:
- 3x MH-Sensor-Series "Flying Fish"

### Key Components
#### Imports and Initialization
- **Imports**: The script imports necessary modules including random, socket, and time.
- **Initialization**: Initializes a socket for server operations.
#### Probability List Generation
- **`probability_to_list(probability, length=100) -> list[bool]`:** Generates a list of boolean values based on a 
specified probability for simulating sensor data updates and heartbeat signals.
- **`get_sensor_data() -> tuple[int, ...]`:** Retrieves sensor data from specified IO pins or hardware inputs, either in
a simulated sandbox mode or directly from hardware IO pins.
- **`handler(client: socket.socket)`:** Handles communication with a connected client. Sends sensor data and handles 
heartbeat messages.
#### Main Loop
Continuously listens for and accepts client connections, handling each connection with the handler function.

---
# Future Enhancements
## Live-View Website Integration
Integrate a web-based dashboard to provide a live view of the robot's current sensor states, motor speeds, and 
gyroscopic angle. This dashboard will allow remote monitoring and control, enhancing the user interface and interaction 
with the robot system.
### Key Components
- **Web Framework**: Utilize frameworks like [Flask](https://pypi.org/project/Flask/) or 
[Django](https://pypi.org/project/Django/) to build a web server.
- **Socket Communication**: Extend the existing socket communication to include a web client that can receive sensor 
data updates.
- **Real-Time Updates**: Implement WebSocket technology for real-time updates of sensor states, motor speeds, and 
gyroscopic angle on the web interface.
- **Visualization**: Display sensor data in graphical formats (e.g., charts for gyro angle, speed gauges for motors).
### Benefits
- **Remote Monitoring**: Users can monitor the robot's status and environment from a web browser.
- **Interactive Control**: Enable basic control functionalities (e.g., start/stop motors, initiate turns) via the web 
interface.
- **Enhanced User Experience**: Provide a more intuitive and informative user interface for interacting with the robot.
## Advanced Navigation and Path Planning Algorithm
Enhance the existing algorithm with advanced navigation and path-planning capabilities to improve the robot's autonomy 
and decision-making in complex environments.
### Key Components
- **Mapping**: Implement simultaneous localization and mapping (SLAM) techniques to create a map of the robot's 
environment.
- **Dynamic Replanning**: Implement mechanisms for dynamic replanning in response to changing environmental conditions 
or unexpected obstacles.
### Benefits
- **Improved Autonomy**: Enable the robot to navigate efficiently and autonomously in varied environments.
- **Safety**: Enhance safety by reducing the likelihood of collisions and improving obstacle avoidance.
- **Scalability**: Prepare the robot for more complex tasks and environments with scalable navigation capabilities.

---
# Conclusion
This project demonstrates a practical implementation of a robot control system integrated with real-time sensor data 
streaming. The scripts work in tandem to facilitate autonomous robot navigation and environmental awareness. The use of 
TCP-communication enables seamless data exchange between the robot and the sensor-module, enhancing the robot's ability 
to react to its surroundings dynamically.
By integrating a live-view website and advancing the navigation algorithm, this project can significantly enhance the 
functionality and performance of the robot control system. These enhancements will not only improve user interaction and
monitoring but also enable the robot to operate more effectively in real-world scenarios, making it a more capable and
versatile tool for various applications.
