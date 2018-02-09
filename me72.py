from kwp2000 import *
import time
import struct
from struct import unpack

#
# Bosch Motronic v7.2 (M62TU) - KWP2000 protocol
#

class ME72(KWP2000):
	def run(self):
		for address in [ DME ]:
			print("Querying DME " + hex(address))
			source = bytes(b'\xf1')
			self._execute(address, source, bytes(b'\xa2')) # b8 12 f1 01 a2 f8
			time.sleep(0.2)
			self._execute(address, source, bytes(b'\x22\x40\x00')) # b8 12 f1 03 22 40 00 3a
			time.sleep(0.2)
			self._execute(address, source, bytes(b'\x22\x40\x03'))
			time.sleep(0.2)
			self._execute(address, source, bytes(b'\x22\x40\x04'))
			time.sleep(0.2)
			self._execute(address, source, bytes(b'\x22\x40\x05'))
			time.sleep(0.2)
			self._execute(address, source, bytes(b'\x22\x40\x07')) # b8 12 f1 03 22 40 07 3d 
			time.sleep(0.2)
			self._execute(address, source, bytes(b'\x21\x13'))
			time.sleep(0.2)
			self._execute(address, source, bytes(b'\x21\x14'))
			time.sleep(0.2)

	def simulator(self):
		payload = super(ME72, self).simulator()
		if payload is None:
			return
		if payload == bytes(b'\x22\x40\x00'):
			reply = bytearray(b'\xb8\xf1\x12\x2d\x62\x40\x00\x00\xc3\x7e\x36\x81\xb4\x00\x0a\xec\x46\xff\xf1\x00\x21\x66\xc4\x11\x05\x00\xb5\x1b\x62\x8f\x00\x93\xaf\x00\x20\x00\x1f\x00\x1e\x00\x1f\x00\x25\x00\x1e\x00\x24\x00\x1e\x93')
		elif payload == bytes(b'\x22\x40\x03'):
			reply = bytearray(b'\xb8\xf1\x12\x18\x62\x40\x03\xff\x70\xff\x4e\x00\x00\xff\xd8\x00\x32\x00\x90\x00\x0c\x00\x8e\x01\x00\xe5\x01\x26\x98')
		elif payload == bytes(b'\x22\x40\x04'):
			reply = bytearray(b'\xb8\xf1\x12\x13\x62\x40\x04\x00\x2c\x00\x20\x82\x83\x80\x0c\x6c\x6c\x6c\x6c\x00\xf5\x01\x15\x0e')
		elif payload == bytes(b'\x22\x40\x05'):
			reply = bytearray(b'\xb8\xf1\x12\x0b\x62\x40\x05\x2b\x00\x00\xf2\xf2\xce\xf8\x20\x4a')
		elif payload == bytes(b'\x22\x40\x07'):
			reply = bytearray(b'\xb8\xf1\x12\x05\x62\x40\x07\xfd\x10\x96')
		else:
			return
		self._device.write(reply)

	def _execute(self, address, source, payload):
		reply = super(ME72, self)._execute(address, source, payload)
		if reply is None:
			return

		p = reply[4:]
		if payload == bytes(b'\xa2'):
			"""
				b8 12 f1 01 a2 f8

				b8 f1 12 2b  
				e2 
				37 35 30 36 33 36 36 # 7506366 part number
				30 46 # 0F hardware number
				30 31 # 01 coding index
				41 38 # A8 diag number
				36 30 # 60 bus index
				30 38 # 08 build date.week
				30 30 # 00 build date.year
				30 30 31 30 32 31 # 001031 supplier
				33 35 31 30 
				ff ff # software number
				ff ff 30 30 30 30 38 33 38 32 38 99
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
			supplier = p[20:26]
			print("supplier : " + supplier.decode('utf-8'))
		
		elif payload == bytes(b'\x22\x40\x00'):
			"""
				b8 12 f1 03 22 40 00 3a

				b8 f1 12 2d                
				62 40 00 
				00 00 # injection time 
				80 00 # Lambdaintegrator 1  
				80 00 # Lambdaintegrator 2
				00 # speed
				00 00 # current rpm
				50 # target rpm
				00 00 # bsnk 1 camshift intake position  
				00 00 # bsnk 2 camshift intake position
				65 # intake air tempature
				60 # coolant temperature 
				00 # ignition angle 
				05 # throttle angle 
				00 00 # air mass
				a8 d1 # Load 
				7f # Battery voltage 
				00 94 # pedal position
				5e # coolant outlet temperature
				0c 80 0c 80 0c 80 0c 80 0c 80 0c 80 0c 40 0c 80 # knock sensor of 8 cyl
				08 # check sum
			"""
			injection_time = struct.unpack('>H'*1, p[3:5])
			print("injection time : " + str(injection_time[0] * 0.016) + " ms")
			speed = p[9]
			print("speed : " + str(speed * 1.25) + " km/h")
			rpm = struct.unpack('>H'*1, p[10:12])
			print("current rpm : " + str(rpm[0] * 0.25) + " RPM")
			target_rpm = p[12]
			print("target rpm : " + str(target_rpm * 10) + " RPM")
			intake_air_temp = p[17]
			print("intake air temp : " + str(intake_air_temp * 0.75 - 48.0) + " C")
			coolant_temp = p[18]
			print("coolant temp : " + str(coolant_temp * 0.75 - 48.0) + " C")
			#ignation_angle = struct.unpack('>b'*1, str(p[19]))
			ignation_angle = byte_to_int(p[19])
			print("ignation angle : " + str(ignation_angle * 0.75) + " Grad")
			engine_throttle_angle = p[20]
			print("engine throttle angle : " + str(engine_throttle_angle * 0.39216) + " %")
			engine_air_mass = struct.unpack('>H'*1, p[21:23])
			print("engine air mass : " + str(engine_air_mass[0] * 0.1) + " kg/h")
			load = struct.unpack('>H'*1, p[23:25])
			print("load : " + str(load[0] * 0.0015259) + " %")
			battery_voltage = p[25]
			print("battery voltage : " + str(battery_voltage * 0.095) + " V")
			pedal_position = struct.unpack('>H'*1, p[26:28])
			print("pedal position : " + str(pedal_position[0] * 0.0048828) + " V")
			coolant_outlet_temp = p[28]
			print("coolant outlet temp : " + str(coolant_outlet_temp * 0.75 - 48.0) + " C")

			r = struct.unpack('>H'*1, p[29:31])
			print("Knock sensor Cyl. 1 : " + str(r[0] * 0.019531) + " V")
			r = struct.unpack('>H'*1, p[31:33])
			print("Knock sensor Cyl. 2 : " + str(r[0] * 0.019531) + " V")
			r = struct.unpack('>H'*1, p[33:35])
			print("Knock sensor Cyl. 3 : " + str(r[0] * 0.019531) + " V")
			r = struct.unpack('>H'*1, p[35:37])
			print("Knock sensor Cyl. 4 : " + str(r[0] * 0.019531) + " V")
			r = struct.unpack('>H'*1, p[37:39])
			print("Knock sensor Cyl. 5 : " + str(r[0] * 0.019531) + " V")
			r = struct.unpack('>H'*1, p[39:41])
			print("Knock sensor Cyl. 6 : " + str(r[0] * 0.019531) + " V")
			r = struct.unpack('>H'*1, p[41:43])
			print("Knock sensor Cyl. 7 : " + str(r[0] * 0.019531) + " V")
			r = struct.unpack('>H'*1, p[43:45])
			print("Knock sensor Cyl. 8 : " + str(r[0] * 0.019531) + " V")
			
		elif payload == bytes(b'\x22\x40\x03'):
			r = struct.unpack('>h'*1, p[3:5])
			print("Roughness Cyl. 1 : " + str(r[0] * 0.0027756) + " sec-1")
			r = struct.unpack('>h'*1, p[5:7])
			print("Roughness Cyl. 2 : " + str(r[0] * 0.0027756) + " sec-1")
			r = struct.unpack('>h'*1, p[7:9])
			print("Roughness Cyl. 3 : " + str(r[0] * 0.0027756) + " sec-1")
			r = struct.unpack('>h'*1, p[9:11])
			print("Roughness Cyl. 4 : " + str(r[0] * 0.0027756) + " sec-1")
			r = struct.unpack('>h'*1, p[11:13])
			print("Roughness Cyl. 5 : " + str(r[0] * 0.0027756) + " sec-1")
			r = struct.unpack('>h'*1, p[13:15])
			print("Roughness Cyl. 6 : " + str(r[0] * 0.0027756) + " sec-1")
			r = struct.unpack('>h'*1, p[15:17])
			print("Roughness Cyl. 7 : " + str(r[0] * 0.0027756) + " sec-1")
			r = struct.unpack('>h'*1, p[17:19])
			print("Roughness Cyl. 8 : " + str(r[0] * 0.0027756) + " sec-1")
		
		elif payload == bytes(b'\x22\x40\x04'):
			r = struct.unpack('>h'*1, p[3:5])
			print("Adaptation additive 1 : " + str(r[0] * 0.046875) + " %")
			r = struct.unpack('>h'*1, p[5:7])
			print("Adaptation additive 2 : " + str(r[0] * 0.046875) + " %")
			r = struct.unpack('>h'*1, p[7:9])
			print("Adaptation multiplicative 1 : " + str(r[0] * 0.0000305) + " %")
			r = struct.unpack('>h'*1, p[9:11])
			print("Adaptation multiplicative 2 : " + str(r[0] * 0.0000305) + " %")

		elif payload == bytes(b'\x22\x40\x05'):
			r = p[9]
			print "leak diagnostic pump : %s" % ("On" if (r & 0x01) > 0 else "Off")
			print "secondary air pump value : %s" % ("On" if (r & 0x02) > 0 else "Off")
			print "oxgen sensor heater before bank 1 : %s" % ("On" if (r & 0x10) > 0 else "Off")
			print "oxgen sensor heater before bank 2 : %s" % ("On" if (r & 0x20) > 0 else "Off")
			print "oxgen sensor heater after bank 1 : %s" % ("On" if (r & 0x40) > 0 else "Off")
			print "oxgen sensor heater after bank 2 : %s" % ("On" if (r & 0x80) > 0 else "Off")
			r = p[10]
			print "exhaust gas recirculation : %s" % ("On" if (r & 0x08) > 0 else "Off")
			print "electric fan : %s" % ("On" if (r & 0x10) > 0 else "Off")
			print "fuel pump : %s" % ("On" if (r & 0x20) > 0 else "Off")
			print "thermostat : %s" % ("On" if (r & 0x40) > 0 else "Off")
			print "start mode : %s" % ("On" if (r & 0x80) > 0 else "Off")

		elif payload == bytes(b'\x22\x40\x07'):
			"""
			b8 f1 12 05 62 40 07 01 90 ea
			"""
			b = p[3]
			print("neutral switch : " + str(b & (1 << 0)))
			print("acceleration enrichment : " + str(b & (1 << 1)))
			print "oxygen sensor after bank 2 ready : %s" % ("Yes" if(b & (1 << 2)) > 0 else "No")
			print "oxygen sensor after bank 1 ready : %s" % ("Yes" if(b & (1 << 3)) > 0 else "No")
			print "oxygen sensor before bank 2 ready : %s" % ("Yes" if(b & (1 << 4)) > 0 else "No")
			print "oxygen sensor before bank 1 ready : %s" % ("Yes" if(b & (1 << 5)) > 0 else "No")
		elif payload == bytes(b'\x21\x13'):
			r = p[2]
			print("verification time VANOS 1 : " + str(r))
			r = p[3]
			print("verification time VANOS 2 : " + str(r))
			r = struct.unpack('>h'*1, p[4:6])
			print("early time 1 : " + str(r[0] * 0.01) + " secs")
			r = struct.unpack('>h'*1, p[6:8])
			print("early time 2 : " + str(r[0] * 0.01) + " secs")
			r = struct.unpack('>h'*1, p[8:10])
			print("delay time 1 : " + str(r[0] * 0.01) + " secs")
			r = struct.unpack('>h'*1, p[10:12])
			print("delay time 2 : " + str(r[0] * 0.01) + " secs")
		elif payload == bytes(b'\x21\x14'):
			r = p[2]
			print("VANOS 1 tightness : " + str(r))
			r = p[3]
			print("VANOS 2 tightness : " + str(r))
			r = struct.unpack('>h'*1, p[4:6])
			print("actual angle for VANOS 1 : " + str(r[0] * 0.0039) + " GrandKW")
			r = struct.unpack('>h'*1, p[6:8])
			print("actual angle for VANOS 2 : " + str(r[0] * 0.0039) + " GrandKW")
		else:
			print("Unknown payload")
