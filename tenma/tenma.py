# class for interfacing with Tenma 72-13360 60V DC power supply.
# updated version with method to generate electrical impulses
# Copyright Diogo Fonseca, 2025

import time
import serial


class Tenma:
    # class variables

    def __init__(self):
        # instance variables
        self.obj = object()  # will store serial object when handshake method is called
        self.connected = False

    def handshake(self, port):  # returns true if connection is successful
        try:
            self.obj = serial.Serial(port=port, baudrate=115200, timeout=.1)
            start_time = time.time()

            while not self.connected:
                msg = b"*IDN05?\n"
                self.obj.write(msg)
                msg = self.obj.readline()
                self.connected = (
                    msg == b'TENMA 72-13360 V2.2 SN:000003342408\n')
                if time.time() - start_time > 3:
                    raise Exception
            print("successfully connected")
            return True
        except:
            print("connection failed")
            return False

    # Enable output
    def out(self, flag):
        # concatenate string
        # multiply flag by 1 so that bool "True/False" are also converted to "1/0"
        msg = "OUT05:" + str(flag * 1)
        # add LF terminator
        msg = msg + "\n"
        # convert to byte
        msg = msg.encode()
        # send to device
        self.obj.write(msg)

    # Set Voltage
    def vset(self, voltage):
        # concatenate string
        msg = "VSET05:" + str(voltage)
        # add LF terminator
        msg = msg + "\n"
        # convert to byte
        msg = msg.encode()
        # send to device
        self.obj.write(msg)

    # Set Current
    def iset(self, current):
        # concatenate string
        msg = "ISET05:" + str(current)
        # add LF terminator
        msg = msg + "\n"
        # convert to byte
        msg = msg.encode()
        # send to device
        self.obj.write(msg)

    # Read Voltage
    def vget(self):
        # concatenate string
        msg = "VOUT05?"
        # add LF terminator
        msg = msg + "\n"
        # convert to byte
        msg = msg.encode()
        # send to device
        self.obj.write(msg)
        # read response from device
        try:
            msg = self.obj.readline()
            msg = float(msg)
            return msg
        except:
            return -1
            pass

    # Read Current
    def iget(self):
        # concatenate string
        msg = "IOUT05?"
        # add LF terminator
        msg = msg + "\n"
        # convert to byte
        msg = msg.encode()
        # send to device
        self.obj.write(msg)
        # read response from device
        try:
            msg = self.obj.readline()
            msg = float(msg)
            return msg
        except:
            return -1
            pass

    # Read Resistance
    def rget(self):
        volts = self.vget()
        amps = self.iget()
        try:
            ohms = volts / amps
            return ohms
        except:
            return -1

    # Read Power
    def pwrget(self):
        volts = self.vget()
        amps = self.iget()
        try:
            watts = volts * amps
            return watts
        except:
            return -1

    # Generate single electrical impulse
    def impulse(self, voltage, current, period):
        self.out(False)  # ensure power off starting condition
        self.vset(voltage)  # set voltage
        self.iset(current)  # set current

        # main loop
        try:
            self.out(True)  # turn power on
            t_start = time.time()  # save starting time
            while time.time()-t_start < period:
                pass  # do nothing while end condition is not met
            self.out(False)  # turn off power at the end of the impulse
            print("impulse cycle completed")
        except KeyboardInterrupt:
            self.out(False)
            print("test stopped by the user")

    # close serial connection
    def close_connection(self):  # TODO
        if self.connected:
            self.obj.close()
            print('Tenma connection closed')
        pass
