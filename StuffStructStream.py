from OutputStream import OutputStream
import ftj


# 这部分代码不要问我命名风格为什么奇怪, 不要问我代码到底啥意思, 我也不知道...
# 代码根据反编译JAVA代码来的, 就硬抄, 硬翻译

class a:
    a = 0
    b = 0
    c = 0

    def __init__(self, decode_Data):
        self.a = decode_Data.readUnsignedShort()
        self.b = decode_Data.readByte()
        self.c = decode_Data.readByte()


class StuffStructStream:
    a = b''
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    h = []
    i = 0

    def a_out(self, decode_Data):
        v3 = decode_Data.readBytes(4)
        v1 = 0
        v2 = 0
        while v1 < 4:
            v0 = v2 << 8
            if v3[v1] < 0:
                v0 += 0x100
            v2 = v3[v1] + v0
            v1 += 1
        return v2

    def a_i_i(self, arg3, arg4):
        if arg3 > 9 or arg3 < 1 or arg4 > 9 or arg4 < -1:
            return ''
        elif arg4 <= -1:
            return "cv" + arg3 + "."
        else:
            return "cv" + arg3 + "." + arg4

    def b_out(self, decode_Data):
        if not self.c_i_i(3, -1):
            return decode_Data
        v7 = self.i - decode_Data.available()
        if v7 >= self.e:
            return decode_Data
        v0 = self.e - v7
        v1 = decode_Data.readBytes(v0)
        v3 = self.f * self.b
        v4 = decode_Data.readInt()
        v5 = self.a_out(decode_Data)
        v6 = v5 + 1
        v6_1 = decode_Data.readBytes(decode_Data.available())
        v8 = b''
        for index in range(v6):
            v8 += b'\x00'
        ret, v6_1, v8 = ftj.ftj_b(v6_1, 0, v4, v8, v5)
        if ret != v3:
            return decode_Data
        v9 = b''
        for index in range(v3 + v0 + 4):
            v9 += b'\x00'
        v9 = bytearray(v9)
        v9[:len(v1)] = bytearray(v1)
        v1_1 = 0
        v3 = 0
        while v3 < self.f:
            v4 = 0
            v5 = v0
            while v4 < self.b:
                v9[v5: v5 + 1] = v8[v1_1: v1_1 + 1]
                v5 += self.f
                v4 += 1
                v1_1 += 1
            v3 += 1
            v0 += 1
        self.i = len(v9) + v7
        decode_Data = OutputStream(bytes(v9))
        return decode_Data

    def b_i_i(self, arg3, arg4):
        if arg3 > 9 or arg3 < 1 or arg4 > 9 or arg4 < -1:
            return ''
        elif arg4 <= -1:
            return "tb" + str(arg3) + "."
        else:
            return "tb" + str(arg3) + "." + str(arg4)

    def c(self, decode_Data):
        self.a = decode_Data.readBytes(6)
        self.b = decode_Data.readInt()
        self.c = decode_Data.readLong()
        self.d = decode_Data.readInt()
        self.e = decode_Data.readUnsignedShort()
        self.f = decode_Data.readUnsignedShort()
        self.g = decode_Data.readUnsignedShort()

        for temp in range(self.g):
            temp = a(decode_Data)
            self.h.append(temp)

    def c_i_i(self, arg5, arg6):
        if 1 <= arg5 <= 9 and -1 <= arg6 <= 9 and len(self.a) != 0:
            v1 = ''
            v2_1 = str(self.a, encoding='gbk')
            if v2_1[0:2] == 'tb':
                v1 = self.b_i_i(arg5, arg6)
            elif v2_1[0:2] == 'cv':
                v1 = self.a_i_i(arg5, arg6)
            if v1 == '':
                return False
            if arg6 >= 0:
                return v2_1 == v1
            return v2_1[0:4] == v1[0:4]

    def d(self, decode_Data):
        if decode_Data.available() < 28:
            return decode_Data
        self.i = decode_Data.available()
        self.c(decode_Data)
        decode_Data = self.b_out(decode_Data)
        return decode_Data
