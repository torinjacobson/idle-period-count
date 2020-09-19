import json
import os

from saleae.range_measurements import DigitalMeasurer
from saleae.data import GraphTimeDelta

import appdirs

IDLE_PERIODS = "idlePeriods"
DEFAULT_IDLE_PERIOD_THRESHOLD_US = 1000

class IdlePeriodConfigurationFile:
    def __init__(self):
        self.default_location = appdirs.user_data_dir("IdlePeriodCount", "BlackbeardSoftware")
        self.config_file = os.path.join(self.default_location, "config.json")
    
    def config_file_exists(self):
        return os.path.isfile(self.config_file)
    
    def load(self):
        f = open(self.config_file)
        config_data = IdlePeriodConfiguration()

        config_data.deserialize(f.read())
        return config_data
    
    def save(self, config_data):
        f = open(self.config_file, "w")
        f.write(config_data.serialize())
    
    def create_config_file(self):
        if not os.path.isdir(os.path.dirname(self.config_file)):
            os.makedirs(os.path.dirname(self.config_file))
        config_data = IdlePeriodConfiguration()
        self.save(config_data)

class IdlePeriodConfiguration:
    def __init__(self):
        # Add configuration data here
        self.time_threshold_us = DEFAULT_IDLE_PERIOD_THRESHOLD_US
    
    def serialize(self):
        return json.dumps(
            {
                # Add configuration data here
                "time_threshold_us": self.time_threshold_us
            }
            , indent=2)
    
    def deserialize(self, json_string):
        d = json.loads(json_string)
        # Add configuration data here
        self.time_threshold_us = d["time_threshold_us"]

class IdlePeriodCount(DigitalMeasurer):
    supported_measurements = [IDLE_PERIODS]

    # Initialize your measurement extension here
    # Each measurement object will only be used once, so feel free to do all per-measurement initialization here
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)

        self.last_edge = None
        self.idle_periods = 0

        self.load_config()

    def load_config(self):
        config_file = IdlePeriodConfigurationFile()
        if not config_file.config_file_exists():
            config_file.create_config_file()
        config_data = config_file.load()

        # Add configuration data here
        self.time_threshold = GraphTimeDelta(microsecond=config_data.time_threshold_us)

    # This method will be called one or more times per measurement with batches of data
    # data has the following interface
    #   * Iterate over to get transitions in the form of pairs of `Time`, Bitstate (`True` for high, `False` for low)
    # `Time` currently only allows taking a difference with another `Time`, to produce a `float` number of seconds
    def process_data(self, data):
        for t, bitstate in data:
            if not self.last_edge is None:
                idle_time = t- self.last_edge
                if idle_time > self.time_threshold:
                    self.idle_periods += 1
            self.last_edge = t
        pass

    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        values = {}
        if IDLE_PERIODS in self.requested_measurements:
            values[IDLE_PERIODS] = self.idle_periods
        return values
