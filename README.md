
# Idle Period Count

A Saleae Digital Measurment extension to count periods of idle activity on a clock signal, data line, etc.

* Ni is the number of idle periods (negative or positive pulses really)
* Ti is the total amount of time spent idle

By default, the threshold for the idle period is 1 millisecond (1000
microseconds). This can be modified by editting the configuration file:
* Windows: ```C:\Users\<USERNAME>\AppData\Local\BlackbeardSoftware\IdlePeriodCount\config.json```
* MacOS: ```~/Library/ApplicationSupport/IdlePeriodcount/config.json```

The time_threshold_us item must be modified. The units are microseconds

```
{
  "time_threshold_us": 1000
}
```
