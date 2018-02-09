from k_line import *

#
# KWP2000
#

class KWP2000(K_Line):
	def sniffer(self):
		print("KWP2000 sniffer ...")
		self._read()

	def simulator(self):
		reply = self._read()
		if reply is None:
			# print("No response - Invalid Address ...")
			return None
		header = reply[0]
		if header != 0xB8:
			print("Unexpected header")
			return None
		return reply

	def _write(self, address, source, payload):
		p = bytearray()
		p.append(0xb8)
		p.append(address)
		p.append(source)
		p.append(len(payload))
		for x in payload:
			p.append(x)
		p.append(self._checksum(p))
		print("TX : " + ''.join('{:02x} '.format(x) for x in p))

		self._device.write(p)        
		return 

	def _read(self):
		p = bytearray()
		try:
			header = self._device.read(1)[0]
			p.append(header)
			source = self._device.read(1)[0]
			p.append(source)
			address = self._device.read(1)[0]
			p.append(address)
			size = self._device.read(1)[0]
			p.append(size)
			remaining = ord(size)
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

	def _execute(self, address, source, payload):
		self._write(address, source, payload)
		echo = self._read()
		#self._device.timeout = 0.1
		reply = self._read()
		if reply is None:
			print("No response - Invalid Address ...")
			return None
		header = reply[0]
		if header != 0xB8:
			print("Unexpected header")
			return None
		return reply
