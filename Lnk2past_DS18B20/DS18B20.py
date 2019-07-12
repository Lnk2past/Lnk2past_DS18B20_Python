import pathlib
import re

DEVICES_HOME = pathlib.Path('/sys/bus/w1/devices/')
TEMPERATURE_RE = re.compile('t=(\d+)')


def get_all_sensors():
    sensors = DEVICES_HOME.glob('28-*/w1_slave')
    return sensors


class DS18B20:
    def __init__(self, sensor, celsius=True):
        self.sensor = sensor
        self.handle = open(str(sensor), 'r')
        self.unit = celsius
        
    def read_temperature(self):
        self.handle.seek(0)
        content = self.handle.read()
        match = TEMPERATURE_RE.search(content)
        temp = float(match.group(1)) / 1000.0
        return temp if self.unit else DS18B20.to_fahrenheit(temp)

    @staticmethod
    def to_fahrenheit(c):
        return (c * 9.0 / 5.0) + 32.0

# sensors = get_all_sensors()
# for s in sensors:
#     p = DS18B20(s)
#     while True:
#         print(p.read_temperature(False))
