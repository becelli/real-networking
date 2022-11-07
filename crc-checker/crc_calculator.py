from dataclasses import dataclass
from abc import ABC, abstractmethod
class CRC(ABC):
  
  @abstractmethod
  def encode(self) -> bytes:
    pass

  @abstractmethod
  def validate(self) -> bool:
    pass


class CRC32(CRC):
  def __init__(self, data: str = None, binary: bytes = None):
    self.data = data if data else binary.decode()
    self.crc = 0
    self.generator = b'100000100110000010001110110110111'

  def encode(self) -> bytes:
    self.crc = self.crc32(self.data)
    return self.crc.to_bytes(4, 'big')

  def validate(self, binary: bytes) -> bool:
    return self.crc == self.crc32(self.data)

  def crc32(self, data: str) -> int:
    crc = 0
    for byte in data.encode():
      crc = crc ^ byte
      for _ in range(8):
        if crc & 1:
          crc = (crc >> 1) ^ int(self.generator, 2)
        else:
          crc >>= 1
    return crc

    