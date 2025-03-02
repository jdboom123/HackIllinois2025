import typing
import gpiozero
from rover import _constants
from typing import TypeVar


class BoundedInt(int):
    MIN: int
    MAX: int

    def __new__(cls, value: int) -> int:
        if not (cls.MIN <= value <= cls.MAX):
            raise ValueError(
                f"{cls.__name__} must be {cls.MIN} <= `{cls.__name__}` <= {cls.MAX}, got {value}")
        return int(value)


class BoundedFloat(float):
    MIN: int
    MAX: int

    def __new__(cls, value: float) -> float:
        if not (cls.MIN <= value <= cls.MAX):
            raise ValueError(
                f"{cls.__name__} must be {cls.MIN} <= `{cls.__name__}` <= {cls.MAX}, got {value}")
        return float(value)


class UnsignedSpeed(BoundedInt):
    MIN = 0
    MAX = _constants.ABSOLUTE_MAX_MOTOR_SPEED


class SignedSpeed(BoundedInt):
    MIN = -_constants.ABSOLUTE_MAX_MOTOR_SPEED
    MAX = _constants.ABSOLUTE_MAX_MOTOR_SPEED


class ServoID(BoundedInt):
    MIN = 1
    MAX = _constants.N_SERVOS


class ServoAngle(BoundedInt):
    MIN = 0
    MAX = 180


class SonarLEDID(BoundedInt):
    MIN = 1
    MAX = _constants.N_SONAR_LEDS


class MotorID(BoundedInt):
    MIN = 1
    MAX = _constants.N_MOTORS


class Heading(BoundedFloat):
    MIN = 0.0
    MAX = 360.0


class MotorConfig(typing.TypedDict):
    _ID: int
    _POLARITY: bool
    _FORCE_HEADING: Heading


class AxleConfig(typing.TypedDict):
    left: MotorConfig
    right: MotorConfig


class DrivetrainConfig(typing.TypedDict):
    front: AxleConfig
    rear: AxleConfig


RGB_COLORS = typing.Literal['red', 'green', 'blue']


class CameraServoIds(typing.TypedDict):
    pan: int
    tilt: int


class KeyPins(typing.TypedDict):
    key1: gpiozero.Pin
    key2: gpiozero.Pin


class PixelStrip(typing.TypedDict):
    COUNT: int
    PIN: int
    FREQ_HZ: int
    DMA: int
    BRIGHTNESS: int
    CHANNEL: int
    INVERT: bool
