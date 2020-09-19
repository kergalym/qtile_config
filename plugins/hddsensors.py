# -*- coding:utf-8 -*-
# Copyright (c) 2012 TiN
# Copyright (c) 2012, 2014 Tycho Andersen
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2014-2015 Sean Vig
# Copyright (c) 2014 Adi Sieker
# Copyright (c) 2014 Foster McLane
# Copyright (c) 2017 Galym Kerimbekov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os.path import isabs
from six import PY2
from . import base
from ..utils import UnixCommandNotFound, catch_exception_and_warn
import re


class HDThermalSensor(base.InLoopPollText):
    """This widget mostly based on `widget.ThermalSensor()` and use
    hddtemp to display HDD temperature,

    For using this thermal sensor widget you need to have hddtemp installed.
    You can get a list of the drive_names executing "hddtemp --odgt" in your
    terminal. Then you can choose which you want, otherwise it will display
    the first available.
    """
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('drive_name', '/dev/sda',
            'Full path to the drive. For example: "/dev/sda"'),
        ('threshold', 60,
            'If the current temperature value is above, '
            'then change to foreground_alert colour'),
        ('foreground_alert', 'ff0000', 'Foreground colour alert'),
        ('update_interval', 2, 'Update interval in seconds'),
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(HDThermalSensor.defaults)
        """<drive name>, <describe>, <temp value>, <Celcius>
        """
        self.sensors_temp = re.compile(
            (r"(.*): (.*): ([ \d]+)({degrees}[C]+)"
             ).format(degrees=u"\xc2\xb0" if PY2 else u"\xb0"),
            re.UNICODE | re.VERBOSE
        )
        self.value_temp = re.compile("\d+")
        temp_values = self.get_temp_sensors()
        self.foreground_normal = self.foreground

        if temp_values is None:
            self.data = "hddtemp command not found"
        elif len(temp_values) == 0:
            self.data = "Temperature sensors not found"
        elif self.drive_name is None:
            for k in temp_values:
                self.drive_name = k
                break

    @catch_exception_and_warn(warning=UnixCommandNotFound, excepts=OSError)
    def get_temp_sensors(self):
        """calls the `hddtemp` command with `/dev/sda` arg, so
        the output should be read.
        """

        sensors_out = ''

        if isabs(self.drive_name):
            command = ["/usr/sbin/hddtemp"]
            if command and self.drive_name:
                command.append(str(self.drive_name))
                sensors_out = self.call_process(command)
        else:
            # If we don't have any hard drive just return test output
            sensors_out = '/dev/sda: WDC WD10EZEX-00RKKA0:  45°C'
        return self._format_sensors_output(sensors_out)

    def _format_sensors_output(self, sensors_out):
        """formats output of `hddtemp` command into a dict of
        {<drive_name>: <device model>: (<temperature>,
        <temperature symbol>), ..etc..}
        """
        temperature_values = {}
        print(self.sensors_temp.findall(sensors_out))
        for name, model, temp, symbol in self.sensors_temp.findall(
             sensors_out):
            name = name.strip()
            temperature_values[name] = temp, symbol
        return temperature_values

    def poll(self):
        temp_values = self.get_temp_sensors()
        if temp_values is None:
            return False
        text = ""
        if self.drive_name is not None:
            text += "".join(temp_values.get(self.drive_name, ['N/A']))
        temp_value = float(temp_values.get(self.drive_name, [0])[0])
        if temp_value > self.threshold:
            self.layout.colour = self.foreground_alert
        else:
            self.layout.colour = self.foreground_normal
        return text
