from ds2 import *
import time
import struct
from struct import unpack

#
# Automatic Transmission ZF5HP24 v8.60.2 (E38/E39/E53)
# Gearbox Controller GS8.60.2 for E38, E39
# Decode reference Ecu/GS8602.PRG
#

error_description = {
	0x01:       "Pressure controller EDS 1",
	0x02:       "Pressure controller EDS 2",
	0x03:       "Pressure controller EDS 3",
	0x04:       "Pressure controller EDS 4",
	0x05:       "Pressure controller EDS 5",
	0x0F:       "Pressure controller EDS Total current",
	0x10:       "Solenoid Valve 1",
	0x11:       "Solenoid Valve 2",
	0x12:       "Solenoid Valve 3",
	0x13:       "Lift magnet Shift-Lock",
	0x20:       "Output rev. sensor (n-ab)",
	0x21:       "Turbine rev. sensor",
	0x22:       "Sump oil temperature sensor",
	0x30:       "Torque Converter Clutch - too much slip",
	0x31:       "Symptom gear check",
	0x32:       "Gear Check 1",
	0x33:       "Gear Check 1M/N",
	0x34:       "Gear Check 2",
	0x35:       "Gear Check 3",
	0x36:       "Gear Check 4",
	0x37:       "Gear Check 5",
	0x38:       "Symptom GLUE",
	0x39:       "GLUE-check 2/3",
	0x3A:       "GLUE-check 3/4",
	0x3B:       "Stalling speed",
	0x3C:       "Gearbox Switch",
	0x3D:       "Gearbox temperature check",
	0x50:       "ECU internal error 1 (EPROM)",
	0x51:       "ECU internal error 2 (EEPROM)",
	0x52:       "ECU internal error 3 (Watchdog)",
	0x53:       "ECU internal error 4 (FET)",
	0x60:       "V-Batt. supply Cl. 87",
	0x61:       "V-Batt. supply Cl. 30",
	0x70:       "Program Switch",
	0x71:       "Kick-Down Switch",
	0x72:       "Steptronic Switch",
	0x80:       "CAN-Bus check",
	0x81:       "CAN-Time-Out DME",
	0x82:       "CAN-Time-Out ASC",
	0x90:       "CAN Version error",
	0x93:       "CAN Throttle valve",
	0x94:       "CAN Engine temperature",
	0x95:       "CAN Wheel speeds",
	0x97:       "CAN Brake signal"
}

error_flags = {
	0x01:       "Plausibility",
	0x02:       "Short circuit to batt+",
	0x03:       "Short circuit to ground",
	0x04:       "Open circuit",
	0x05:       "Open circuit or Short circuit to batt+",
	0x06:       "Open circuit or Short circuit to ground",
	0x07:       "Too large",
	0x08:       "Too small",
	0x09:       "No change",
	0x0F:       "No suitable error code",
	0x10:       "Error activates MIL",
	0x20:       "Sporadic error",
	0x40:       "Replacement function active",
	0x80:       "Error present",
	0xFE:       "Gen. error",
	0xFF:       "Unknown"
}

class ZF5HP24(DS2):
	def run(self):
		for address in [ EGS ]:
			print("Querying EGS " + hex(address))
			data = self._execute(address, bytes(b'\x00'))
			time.sleep(0.2)
			data = self._execute(address, bytes(b'\x0B\x03'))
			time.sleep(0.2)
			data = self._execute(address, bytes(b'\x04\x01'))
			time.sleep(0.2)

	def simulator(self):
		payload = super(ZF5HP24, self).simulator()
		if payload is None:
			return
		if payload == bytes(b'\x00'):
			reply = bytearray(b'\x32\x2e\xa0\x31\x34\x32\x33\x39\x35\x33\x32\x42\x30\x30\x31\x31\x36\x30\x34\x38\x39\x39\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x39\x31\x30\x46\x4f\x34\x38\x39\x30\x32\x36\x36\xcb')
		elif payload == bytes(b'\x0B\x03'):
			reply = bytearray(b'\x32\x1c\xa0\x15\x15\x00\x00\x01\x93\x7f\xa8\x01\x01\x01\x01\x0f\x00\x00\xff\x00\xa2\xdc\x01\xc0\x40\x00\x59\x9d')
		elif payload == bytes(b'\x04\x01'):
			reply = bytearray('\x32\x06\xa0\x00\x00\x94')
		else:
			return
		self._device.write(reply)

	def _execute(self, address, payload):
		reply = super(ZF5HP24, self)._execute(address, payload)
		if reply is None:
			return
		p = reply[2:]
		if payload == bytes(b'\x00'):
			"""
				32 04 00 36 
				32 2e 
				a0 # status 
				31 34 32 33 39 35 33 # part number 
				32 42 # hardware number
				30 30 # coding index
				31 31 #diag index 
				36 30 # bus index 
				34 38 # build date week 
				39 39 # build date year 
				30 30 30 30 30 30 30 30 30 30 # life number 
				30 39 # software number 
				31 30 # ai number 
				46 4f 34 38 39 30 32 36 36 # product number 
				cb 
			"""
			part_number = p[1:8]
			print("part number : " + part_number.decode('utf-8'))
			hardware_number = p[8:10]
			print("hardware number : " + hardware_number.decode('utf-8'))
			coding_index = p[10:12]
			print("coding index : " + coding_index.decode('utf-8'))
			diag_index = p[12:14]
			print("diag index : " + diag_index.decode('utf-8'))
			bus_index = p[14:16]
			print("bus index : " + bus_index.decode('utf-8'))
			build_date_week = p[16:18]
			print("build date week : " + build_date_week.decode('utf-8'))
			build_date_year = p[18:20]
			print("build date year : " + build_date_year.decode('utf-8'))
			life_number = p[20:30]
			print("life number : " + life_number.decode('utf-8'))
			software_number = p[30:32]
			print("software number : " + software_number.decode('utf-8'))
			ai_number = p[32:34]
			print("ai number : " + ai_number.decode('utf-8'))
			product_number = p[34:43]
			print('product number : ' + product_number.decode('utf-8'))

		elif payload == bytes(b'\x0B\x03'):
			"""
				32 05 0b 03 3f                
				32 1c 
				a0 # status
				00 # rpm
				00 # input turbine rpm 
				00 # output shift rpm 
				00 4f 
				4b # coolant temperature 
				54 # transmission temperature
				93 01 01 01 01 ff ff ff ff ff
				02 
				dc # shifter program 
				00 # cruise control mode
				80 # current gear | shifter steptronic | kick down | vehicle in curve
				00 # last shift 
				00 # user program | actual program
				59 b5

			"""
			rpm = p[1] # struct.unpack('>B'*1, p[1])
			print("rpm : " + str(rpm * 32) + " RPM")
			input_turbine_rpm = p[2]
			print("input turbine rpm : " + str(input_turbine_rpm * 32) + " RPM")
			output_shift_rpm = p[3]
			print("output shift rpm : " + str(output_shift_rpm * 32) + " RPM")
			coolant_temp = p[6]
			print("coolant temperature : " + str(coolant_temp - 48) + " C")
			transmission_temp = p[7]
			print("transmission temperature : " + str(transmission_temp - 54) + " C")
			cruise_control = p[20]
			if cruise_control == 0x0:
				print("cruise control mode : off")
			elif cruise_control == 0x20:
				print("cruise control mode : on")
			elif cruise_control == 0x40:
				print("cruise control mode : resume")
			elif cruise_control == 0x60:
				print("cruise control mode : accel")
			elif cruise_control == 0x80:
				print("cruise control mode : decel")
			else:
				print("cruise control mode : unknown")

			gear = p[21]            
			g = gear >> 5
			if g == 0x6:
				print("gear : 1")
			elif g == 0x7:
				print("gear : reverse")
			else:
				print("gear : " + str(gear >> 5))

			shifter = gear & 0x3
			if shifter == 0x1:
				print("shifter steptronic : up")
			elif shifter == 0x2:
				print("shifter steptronic : down")
			else:
				print("shifter steptronic : neutral")
			kickdown = gear & 0x10
			print "kickdown : %s" % ("yes" if kickdown > 0 else "No")
			vehicle_in_curve = gear & 0x8
			print "vehicle in curve : %s" % ("yes" if vehicle_in_curve > 0 else "No")

		elif payload == bytes(b'\x04\x01'):
			error_code_count = p[1]
			print("error code count : " + str(error_code_count))
			if len(p) >= 5:
				error_code = p[2:4]
				did = p[2]
				fid = p[3]
				freq = p[4]
				print("(" + str(freg) + ") " + "error code 0 : " + error_code.decode('utf-8') + " : " + error_description[did] + " : " + error_flags[fid])
			if len(p) >= 24:
				error_code = p[21:23]
				did = p[21]
				fid = p[22]
				freq = p[23]
				print("(" + str(freg) + ") " + "error code 1 : " + error_code.decode('utf-8') + " : " + error_description[did] + " : " + error_flags[fid])
			if len(p) >= 43:
				error_code = p[40:42]
				did = p[40]
				fid = p[41]
				freq = p[42]
				print("(" + str(freg) + ") " + "error code 2 : " + error_code.decode('utf-8') + " : " + error_description[did] + " : " + error_flags[fid])
			if len(p) >= 62:
				error_code = p[59:61]
				did = p[59]
				fid = p[60]
				freq = p[61]
				print("(" + str(freg) + ") " + "error code 3 : " + error_code.decode('utf-8') + " : " + error_description[did] + " : " + error_flags[fid])
			if len(p) >= 81:
				error_code = p[78:80]
				did = p[78]
				fid = p[79]
				freq = p[80]
				print("(" + str(freg) + ") " + "error code 4 : " + error_code.decode('utf-8') + " : " + error_description[did] + " : " + error_flags[fid])
		 
		else:
			print("Unknown payload")

