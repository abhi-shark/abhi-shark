import time

class QTPYControl_1:
    """
    Generic class to represent Peripheral 1, a QTPY tasked with reading color
    sensor data 
    and actuating the dispensing, acceptance, and rejection servos.

    serialPort: the serial object representing the QTPY
    """

    def __init__(self, serialport):
        self.serialPort = serialport
        self.cs = 0
        self.ps = 0
        self.color = "NON"

        self.prev_response = "NON"
        self.change = 0
        self.raw_read = 0

    def handle_action(self, response):
        # Set threshold for ball detected and desired color

        self.ps = (response != self.prev_response) and (response != "NON")
        self.cs = (response == self.color)
        # change = (raw_read == 1) and (self.cs != raw_read)

        print("Raw:", self.raw_read)
        print("Change:", self.change)

        # self.cs = self.raw_read and self.change
        # self.ps = (response != "NON") and self.change # TODO: fix me

        self.prev_response = response

    def actuate_servo(self, motor):
        """
        Actuate desired motors
        motor: string "acc", "rej", "dis"
        """
        if motor == "acc":      # Accept pollen
            self.serialPort.write(b'ACC\n')
        elif motor == "rej":    # Reject pollen
            self.serialPort.write(b'REJ\n')
        elif motor == "dis":    # Dispense pollen
            self.serialPort.write(b'DIS\n')
        time.sleep(1.5)


class QTPYControl_2:
    """
    Generic class to represent Peripheral 2, a QTPY tasked with reading
    3 rotary encoder inputs to set 3 RGB LEDs. This also sets the game color,
    given as the plant color for Plant 3.

    serialPort: the serial object representing the QTPY
    """

    def __init__(self, serialport):
        self.serialPort = serialport
        self.ultrasonic = 0
        self.color = "NON"
        self.ps = 0


    def handle_action(self, response):
        # Set des color
        self.color = response

    def set_status(self, cmd):
        """
        Light the status LED appropriately
        :param cmd: string "sort" "go" "stop"
        :return: none, but send serial message
        """

        if cmd == "sort":  # Sort pollen in barn
            self.serialPort.write(b'SOR\n')
        elif cmd == "stop":  # Game is stopped
            self.serialPort.write(b'STO\n')
        elif cmd == "go":  # Game is going, timer active
            self.serialPort.write(b'RUN\n')

