#!/usr/bin/env pybricks-micropython

"""
This script controls a robot using the Pybricks Micropython framework on an EV3 brick.
It utilizes motors for movement, a gyro sensor for orientation, and communicates sensor data over a network socket.

  __
<(o )___
 ( ._> /    @ikonodim
  `---'
"""

import time
import _thread
import socket

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor
from pybricks.parameters import Port

# Initialize hardware components
EV3 = EV3Brick()
GYRO = GyroSensor(Port.S4)
MOTORS = [Motor(Port.A), Motor(Port.D)]

# Constants
PAUSE_BEFORE_TURN = 500 / 1000  # Pause before turning in seconds
SPEED = 150  # Global speed


# Global variables
class _GLOBALS:
    sensors_host = ('192.168.2.152', 2000)  # IP address and port for sensor data communication
    turning = False  # Flag indicating if the robot is currently turning
    sensor_data = (0, 0, 0)  # Tuple to hold sensor data (front, left, right)
    stabilization_angle = 0  # Gyro stabilization angle


GLOBALS = _GLOBALS


def start_both_motors(speed: int) -> None:
    """
    Starts both motors at the given speed.

    :param speed: Speed to run the motors at.
    """
    for motor in MOTORS:
        motor.run(speed)


def stop_both_motors(hold: bool = False) -> None:
    """
    Stops both motors.

    :param hold: If True, motors will hold their position; otherwise, they will stop completely.
    """
    if hold:
        for motor in MOTORS:
            motor.hold()
    else:
        for motor in MOTORS:
            motor.stop()


def set_speed_both_motors(speed: int):
    """
    Sets the speed of both motors.

    :param speed: Speed to set for both motors.
    """
    _ = [m.run(speed) for m in MOTORS]


def turn(speed: int, angle: int) -> None:
    """
    Turns the robot to a specific angle using both motors.

    :param speed: Speed of the motors during turning.
    :param angle: Angle (in degrees) to turn. Positive for right, negative for left.
    """
    global GLOBALS, GYRO, MOTORS

    GLOBALS.turning = True

    if angle < 0:  # Left turn
        MOTORS[0].run(speed * (-1))
        MOTORS[1].run(speed)
        GLOBALS.stabilization_angle -= angle

    if angle > 0:  # Right turn
        MOTORS[1].run(speed * (-1))
        MOTORS[0].run(speed)
        GLOBALS.stabilization_angle += angle

    while not GYRO.angle() in range(angle - 1, angle + 1):
        pass

    set_speed_both_motors(speed)
    GLOBALS.turning = False


def stabilize_motors() -> None:
    """
    Continuously adjusts the robot's orientation using the gyro sensor to maintain stability.
    """
    global GLOBALS, GYRO, MOTORS, SPEED

    while True:
        if not GLOBALS.turning:
            if GYRO.angle() > GLOBALS.stabilization_angle + 4:
                turn(SPEED, GLOBALS.stabilization_angle)
            elif GYRO.angle() < GLOBALS.stabilization_angle - 4:
                turn(SPEED, GLOBALS.stabilization_angle)


def stream_sensor_data() -> None:
    """
    Establishes a socket connection to stream sensor data and continuously updates `GLOBALS.sensor_data`.
    """
    global GLOBALS

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(GLOBALS.sensors_host)

    init = sock.recv(256).decode("utf-8")
    if init.startswith("READY_STREAM||"):
        buffer_size = int(init.split("||")[1])

        sock.send(b"START_BROADCAST")
    else:
        exit(1)

    while True:
        try:
            operation, data = sock.recv(buffer_size).decode("utf-8").split("||")
        except ValueError:
            continue

        if operation == "HB":
            sock.send(str("HB||" + str(int(data) * 2 // 3)).encode("utf-8"))
        if operation == "SD":
            GLOBALS.sensor_data = [int(sv) for sv in data.split(";")]


def algorithm():
    """
    Main algorithm that decides robot actions based on sensor data.
    """
    global GLOBALS, GYRO, SPEED  # Declare global variables used within the function

    while True:  # Loop indefinitely for continuous operation

        # CASE: FRONT_ACTIVE
        if GLOBALS.sensor_data[0] == 1:  # Check if front sensor is active
            if GLOBALS.sensor_data[1] == 0:  # Check if left sensor is inactive
                turn(SPEED, GYRO.angle() - 90)  # Turn left (90 degrees) relative to current angle
            elif GLOBALS.sensor_data[2] == 0:  # Check if right sensor is inactive
                turn(SPEED, GYRO.angle() + 90)  # Turn right (90 degrees) relative to current angle
            else:
                turn(SPEED, GYRO.angle() + 180)  # If both left and right sensors are active, turn around

        # CASE: LEFT_INACTIVE
        if GLOBALS.sensor_data[1] == 0:  # Check if left sensor is inactive
            time.sleep(PAUSE_BEFORE_TURN)  # Pause before initiating turn
            turn(SPEED, GYRO.angle() - 90)  # Turn left (90 degrees) relative to current angle

        # CASE: RIGHT_INACTIVE
        if GLOBALS.sensor_data[2] == 1:  # Check if right sensor is inactive
            time.sleep(PAUSE_BEFORE_TURN)  # Pause before initiating turn
            turn(SPEED, GYRO.angle() + 90)  # Turn right (90 degrees) relative to current angle



def main():
    """
    Main function to start the robot control script.
    """
    global GLOBALS

    start_both_motors(SPEED)

    _thread.start_new_thread(stabilize_motors, ())
    _thread.start_new_thread(stream_sensor_data, ())

    try:
        algorithm()
    finally:
        stop_both_motors()


if __name__ == '__main__':
    main()
