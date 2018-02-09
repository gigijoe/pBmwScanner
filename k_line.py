#-*-coding:utf-8 -*-
import serial

def byte_to_int(char):
	if char > 127:
		return (256-char) * (-1)
	else:
		return char

ZKE = 0x00 # Central Body Electronics / Zentrale Karosserieelektronik
DME = 0x12 # Digital Motor Electronics
CENTRAL_BODY = 0x21
EGS = 0x32 # Electronic Transmission Control - Electronische Getriebe Steuerung
EWS = 0x44 # Electronic Immobiliser / Elektronische Wegfahrsperre
DSC = 0x56 # Dynamic Stability Control
IHKA = 0x5B # Auto Climate Control / Integrierte Heizung Kühlung
IKE = 0x80 # Instrument Cluster
AIRBAG = 0xA4 # Multi Restraint System
LCM = 0xD0 # Light Switching Center / Lichtschaltzentrum
MID = 0xC0 # Multi Information Display
RADIO = 0x68 # Radio
SZM = 0xf5 # Center Console Switching Center

class K_Line(object):
	def __init__(self):
		self._device = serial.Serial("/dev/ttyUSB0", 9600, parity=serial.PARITY_EVEN, timeout=0.5)    

	def _checksum(self, message):
		result = 0
		for b in message:
			result ^= b
		return result
