# EP Solar Tracer 3210an Metrics Writer

This repository contains a Python script that retrieves metrics from an EP Solar charge controller, via modbus, and writes them to [InfluxDB cloud](https://www.influxdata.com/products/influxdb-cloud/).
I'm using this code to pull metrics from a Tracer 3210an charge controller and feed them into InfluxDB. 

In order to connect a computer, such as a Raspberry Pi, to the charge controller, you'll need a modbus (RS-485) interface cable.
I am using a DTECH cable along with an RJ-45 cable to connect my Raspberry Pi to the charge controller.
