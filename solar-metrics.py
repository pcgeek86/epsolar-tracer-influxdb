import minimalmodbus
import serial
from time import sleep
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

influx_uri = 'https://us-central1-1.gcp.cloud2.influxdata.com'
influx_token = 'SET THIS TO YOUR OWN TOKEN'
org = 'SET THIS TO YOUR INFLUXDB ORG'
bucket = 'SET THIS TO YOUR INFLUXDB BUCKET'

influx = InfluxDBClient(influx_uri, influx_token)
writer = influx.write_api(write_options=SYNCHRONOUS)

ins = minimalmodbus.Instrument('/dev/ttyUSB0', 1, debug=False)

ins.serial.baudrate = 115200
ins.serial.bytesize = 8
ins.serial.stopbits = 1
ins.serial.parity = serial.PARITY_NONE
ins.serial.timeout = 1

ins.mode = minimalmodbus.MODE_RTU
ins.clear_buffers_before_each_transaction = True

PV_VOLTAGE = 0x3100
PV_CURRENT = 0x3101

while True:
    pv_voltage = ins.read_register(PV_VOLTAGE, 2, 4, False)
    data = 'array1 pv_voltage={0}'.format(pv_voltage)
    writer.write(bucket, org, data)
    print(pv_voltage)

    pv_current = ins.read_register(PV_CURRENT, 2, 4, False)
    data = 'array1 pv_current={0}'.format(pv_current)
    writer.write(bucket, org, data)
    print(pv_current)

    pv_power_low = ins.read_register(0x3102, 0, 4, False);
    data = 'array1 pv_power={0}'.format(pv_power_low/100)
    writer.write(bucket, org, data)
    print(pv_power_low/100)

    # Battery bank voltage
    battery_voltage = ins.read_register(0x3104, 2, 4, False);
    data = 'array1 battery_voltage={0}'.format(battery_voltage)
    writer.write(bucket, org, data)
    print('Battery voltage: {0}'.format(battery_voltage))

    # Battery current
    battery_current = ins.read_register(0x3105, 2, 4, False);
    data = 'array1 battery_current={0}'.format(battery_current)
    writer.write(bucket, org, data)
    print('Battery current: {0}'.format(battery_current))

    # Battery power (watts)
    battery_power = ins.read_register(0x3106, 0, 4, False) / 100;
    data = 'array1 battery_power={0}'.format(battery_power)
    writer.write(bucket, org, data)
    print('Battery power: {0}'.format(battery_power))

    # Battery charge
    battery_charge = ins.read_register(0x311A, 2, 4, False);
    data = 'array1 battery_charge={0}'.format(battery_charge)
    writer.write(bucket, org, data)
    print('Battery charge: {0}'.format(battery_charge))

    sleep(1)
