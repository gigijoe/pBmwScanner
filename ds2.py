#-*-coding:utf-8 -*-
from k_line import *

#
# DS2
#

class DS2(K_Line):
	def sniffer(self):
		print("DS2 sniffer ...")
		self._read()

	def simulator(self):
		reply = self._read()
		if reply is None:
			# print("No response - Invalid Address ...")
			return None
		return reply

	def _write(self, address, payload):
		size = 2 + len(payload) + 1
		p = bytearray()
		p.append(address)
		p.append(size)
		for x in payload:
			p.append(x)
		p.append(self._checksum(p))
		print("TX : " + ''.join('{:02x} '.format(x) for x in p))
		self._device.write(p)

	def _read(self):
		p = bytearray()
		try:
			address = self._device.read(1)[0]
			p.append(address)
			size = self._device.read(1)[0]
			p.append(size)
			remaining = ord(size) - 3
			if remaining > 0:
				payload = self._device.read(remaining)
				for x in payload:
					p.append(x)
			expected_checksum = self._checksum(p)
			actual_checksum = self._device.read(1)[0]
			p.append(actual_checksum)
		except IndexError:
			return None
		print("RX : " + ''.join('{:02x} '.format(x) for x in p))
		print("RAW : " + ''.join('\\x{:02x}'.format(x) for x in p))
		if ord(actual_checksum) != expected_checksum:
			raise ProtocolError("invalid checksum")
		return p

	def _execute(self, address, payload):
		self._write(address, payload)
		echo = self._read()
		#self._device.timeout = 0.1
		reply = self._read()
		if reply is None:
			print("No response - Invalid Address ...")
			return None
		sender = reply[0]
		length = reply[1]
		status = reply[2]
		if sender != address:
			print("Unexpected address")
			return
		if status != 0xa0:
			if status == 0xa1:
				print("Computer busy")
			elif status == 0xa2:
				print("Invalid parameter")
			elif status == 0xff:
				print("Invalid command")
			else:
				print("Unknown status")
			return None
		return reply
