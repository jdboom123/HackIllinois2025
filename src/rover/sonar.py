import typing
from smbus2 import SMBus, i2c_msg
from rover import constants


class Sonar:

    def __init__(self):
        pass

    def get_distance(self) -> int:
        dist: int = 5000
        try:
            with SMBus(constants.I2C_BUS) as bus:
                msg = i2c_msg.write(constants.SONAR_SYSTEM_I2C_ADDR, [0,])
                bus.i2c_rdwr(msg)
                read = i2c_msg.read(constants.SONAR_SYSTEM_I2C_ADDR, 2)
                bus.i2c_rdwr(read)
                dist = int.from_bytes(
                    bytes(list(read)), byteorder='little', signed=False)
                if dist > 5000:
                    dist = 5000
        except BaseException as e:
            print(e)
        return dist
