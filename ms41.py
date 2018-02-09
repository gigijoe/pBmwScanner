from ds2 import *
import time
import struct
from struct import unpack

#
# MS41
#

class MS41(DS2):
	def run(self):
		for address in [ DME ]:
			print("Querying DME " + hex(address))
			data = self._execute(address, bytes(b'\x00'))
			time.sleep(0.2)
			#raw = b'\x12\x1D\xA0\x02\xBF\x00\x26\x17\xAB\x4E\x41\x59\x02\x49\x07\x24\x6A\x88\x22\x7F\x80\x00\x80\x00\x38\x38\xCE\xCE\x09'
			#raw = b'\x12\x1D\xA0\x03\x20\x00\x24\x10\xA3\x91\x38\x6A\x01\xB9\x00\xCE\x4E\x22\x1E\x88\x8F\x3A\x6D\xBA\x87\x6C\xCE\xCE\xDD'
			#data = struct.unpack('<' + 'B'*len(raw), raw)

	def _execute(self, address, payload):
		reply = super(MS41, self)._execute(address, payload)
		if reply is None:
			return

		p = reply[2:]
		if payload == bytes(b'\xa2'):
			engine_speed = struct.unpack('>H'*1, p[0:2])
			print("engine speed : " + str(engine_speed[0]) + " 1/min")
			vehicle_speed = struct.unpack('>B'*1, p[2])
			print("vehicle speed : " + str(vehicle_speed[0]) + " km/h")
			throttle_position = struct.unpack('>B'*1, p[3])
			print("throttle position : " + str(throttle_position[0] * 0.47) + " %")
			engine_load = struct.unpack('>H'*1, p[4:6])
			print("engine load : " + str(engine_load[0] * 0.021) + " mg/stroke")
			air_temp = struct.unpack('>B'*1, p[6])
			print("air temp : " + str(air_temp[0] * (-0.458) + 108) + " C")
			coolant_temp = struct.unpack('>B'*1, p[7])
			print("coolant temp : " + str(coolant_temp[0] * (-0.458) + 108) + " C")
			ignition_time_advance = struct.unpack('>B'*1, p[8])
			print("ignition time advance : " + str(ignition_time_advance[0] * (0.373) + (-23.6)) + " BTDC")
			injector_pulsewidth = struct.unpack('>H'*1, p[9:11])
			print("injector pulse width : " + str(injector_pulsewidth[0] * 0.00534) + " ms")
			IACV = struct.unpack('>H'*1, p[11:13])
			print("IACV : " + str(IACV[0] * 0.00153) + " %")
			# struct.unpack('>H'*1, p[13:15])
			vanos_angle = struct.unpack('>B'*1, p[15])
			print("vanos angle : " + str(vanos_angle[0] * 0.3745) + " KW degrees")
			battery_voltage = struct.unpack('>B'*1, p[16])
			print("battery voltage : " + str(battery_voltage[0] * 0.10196) + " volts")
			# Lambda Integrator 1
			# Lambda Integrator 2
			lambda_upstream_heater_1 = struct.unpack('>B'*1, p[21])
			print("lambda upstream heater 1 : " + str(lambda_upstream_heater_1[0] * 0.3906) + " %")
			lambda_upstream_heater_2 = struct.unpack('>B'*1, p[22])
			print("lambda upstream heater 2 : " + str(lambda_upstream_heater_2[0] * 0.3906) + " %")
			lambda_downstream_heater_1 = struct.unpack('>B'*1, p[23])
			print("lambda downstream heater 1 : " + str(lambda_downstream_heater_1[0] * 0.3906) + " %")
			lambda_downstream_heater_2 = struct.unpack('>B'*1, p[24])
			print("lambda downstream heater 2 : " + str(lambda_downstream_heater_2[0] * 0.3906) + " %")

		else:
			print("Unknown payload")     
