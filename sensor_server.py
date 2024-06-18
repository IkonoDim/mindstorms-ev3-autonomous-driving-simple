import random
import socket
import time
import sys


# Constants
HB_CHECK_PROBABILITY = 0.05
SENSOR_IOS = (14, 15, 16)

# Check if running on MicroPython; set SANDBOX accordingly
if hasattr(sys, 'implementation') and sys.implementation.name == 'micropython':
    SANDBOX = False

    import machine
else:
    SANDBOX = True


# Initialize socket for server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 2000))
sock.listen(1)


def probability_to_list(probability, length=100) -> list[bool]:
    """
    Generates a list with a given probability of True values.

    :param probability: Probability of True values in the list (0 to 1).
    :param length: Length of the list to generate.
    :return: List of booleans where True appears with the given probability.
    """
    if not 0 <= probability <= 1:
        raise ValueError("Probability must be between 0 and 1.")

    true_count = int(probability * length)
    false_count = length - true_count

    result = [True] * true_count + [False] * false_count
    return result


def get_sensor_data() -> tuple[int, ...]:
    """
    Fetches sensor data from specified IO pins or simulates it and returns it as a tuple of integers.

    :return: Tuple representing sensor data as integers (0 or 1).
    """
    global SANDBOX, SENSOR_IOS

    if SANDBOX:
        return random.choice([(0, 0, 0), (0, 1, 0), (1, 0, 0)])

    return tuple(0 if machine.Pin(io, machine.Pin.OUT).value() == 1 else 1 for io in SENSOR_IOS)


def handler(client: socket.socket) -> None:
    """
    Handles communication with a connected client.

    :param client: The connected client socket.
    """
    client.send(b"READY_STREAM||128")

    data = client.recv(128).decode("utf-8")

    if data == "START_BROADCAST":
        last_result = ()
        while True:
            if random.choice(probability_to_list(HB_CHECK_PROBABILITY)):
                nmb = random.randint(1, 100)
                client.send(str("HB||" + str(nmb)).encode("utf-8"))

                start_time = int(time.time())
                while int(time.time()) < start_time + 5:
                    data = client.recv(128).decode("utf-8").split("||")

                    if data[0] == "HB" and data[1] == str(nmb * 2 // 3):
                        break
                    else:
                        client.close()
                        return
            else:
                sens_data = get_sensor_data()

                if sens_data != last_result:
                    last_result = sens_data
                    client.send(("SD||" + ';'.join([str(d) for d in sens_data])).encode("utf-8"))
                    time.sleep(0.01)


while True:
    try:
        handler(sock.accept()[0])
    except ConnectionResetError:
        pass
