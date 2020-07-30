class OutputStream:
    data = b''
    index = 0

    def __init__(self, InputStream):
        self.data = InputStream
        self.index = 0

    def available(self):
        return len(self.data) - self.index

    def skipBytes(self, number):
        self.index += number

    # 返回指定数量unicode2Utf-8的文本
    def readUnicode2UTF8(self, number):
        temp = ''
        for i in range(number):
            temp += chr(self.readChar())
        return temp

    def readBoolean(self):
        ret = True if int.from_bytes(self.data[self.index: self.index + 1], byteorder='little') == 1 else False
        self.index += 1
        return ret

    def readByte(self):
        ret = self.data[self.index: self.index + 1]
        ret = int.from_bytes(ret, byteorder='little')
        self.index += 1
        return ret

    # python没有char这玩意儿, 直接返回一个int
    def readChar(self):
        ret = int.from_bytes(self.data[self.index: self.index + 2], byteorder='little')
        self.index += 2
        return ret

    def readShort(self):
        ret = int.from_bytes(self.data[self.index: self.index + 2], byteorder='little')
        self.index += 2
        return ret

    def readInt(self):
        ret = int.from_bytes(self.data[self.index: self.index + 4], byteorder='little')
        self.index += 4
        return ret

    def readLong(self):
        hex_str = '0x' + self.data[self.index: self.index + 4].hex()
        ret = eval(hex_str)
        self.index += 4
        return ret

    def readUTF(self):
        return self.readUnicode2UTF8(self.readUnsignedShort())

    def readUnsignedShort(self):
        ret = int.from_bytes(self.data[self.index: self.index + 2], byteorder='little')
        self.index += 2
        return ret

    # 读取指定数量的bytes
    def readBytes(self, number):
        ret = self.data[self.index: self.index + number]
        self.index += number
        return ret

    # 读取指定数量的bytes, 但是不向前滑动
    def readBytesOnly(self, number):
        ret = self.data[self.index: self.index + number]
        return ret
