# Robot Control System with Sensor Data Streaming
## Project Overview
This project involves the development of a robot control system using the Pybricks Micropython framework on an EV3 
brick. The system includes components for motor control, gyro sensor-based orientation stabilization, and sensor data 
streaming over a network socket. The project is divided into two main scripts: one for controlling the robot and another
for simulating a server that streams sensor data to the robot.

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
#### Turning and Stabilization
- **`turn(speed: int, angle: int) -> None`:** Turns the robot to a specific angle.
- **`stabilize_motors() -> None`:** Continuously adjusts the robot's orientation to maintain stability.
#### Sensor Data Streaming
- **`stream_sensor_data() -> None`:** Establishes a socket connection to stream sensor data and updates the global 
sensor data.
#### Main Algorithm
- **`algorithm()`:** Main algorithm that decides robot actions based on sensor data.
- This algorithm continuously monitors sensor data to control a robot's actions. When the front sensor detects an 
obstacle, it checks the left and right sensors: if the left sensor is inactive, the robot turns left by 90 degrees; 
if the right sensor is inactive, it turns right by 90 degrees. If both left and right sensors detect obstacles, the 
robot performs a 180-degree turn. If the left sensor detects no obstacle, the robot pauses briefly before turning left.
Similarly, if the right sensor detects no obstacle, it pauses briefly before turning right. This approach enables the 
robot to navigate around obstacles effectively based on real-time sensor feedback.
#### Main Function
- **`main()`:** Starts the robot control script, initializes motor control and sensor data streaming threads, and runs 
the main algorithm.

---
## Script 2: Sensor Data Streaming Server
### Description
The second application functions as a server that streams real-time sensor data to the robot over a network 
socket. It establishes socket communication to transmit actual sensor data updates and heartbeat signals at regular 
intervals. The script reads sensor data from specified IO pins or hardware inputs, depending on whether it runs on 
MicroPython or another python environment.

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
- **Path Planning**: Integrate algorithms such as [A* (A-star)](https://en.wikipedia.org/wiki/A*_search_algorithm) or 
[Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) to find optimal paths based on mapped data 
and sensor inputs.
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
