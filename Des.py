# 根据反编译的JAVA撸的3DES的代码

bitTable = [0x80, 0x40, 0x20, 16, 8, 4, 2, 1]
bigbyte = [0x800000, 0x400000, 0x200000, 0x100000, 0x80000, 0x40000, 0x20000, 0x10000, 0x8000, 0x4000, 0x2000, 0x1000,
           0x800, 0x400, 0x200, 0x100, 0x80, 0x40, 0x20, 16, 8, 4, 2, 1]
key_table = [56, 0x30, 40, 0x20, 24, 16, 8, 0, 57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43,
             35, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 60, 52, 44, 36, 28, 20, 12, 4, 27, 19,
             11, 3]
left_shift_table = [1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28]
after_shift_table = [13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9, 22, 18, 11, 3, 25, 7, 15, 6, 26, 19, 12, 1, 40, 51, 30,
                     36, 46, 54, 29, 39, 50, 44, 0x20, 0x2F, 43, 0x30, 38, 55, 33, 52, 45, 41, 49, 35, 28, 0x1F]
DES_SPBOX1 = [0x1010400, 0, 0x10000, 0x1010404, 0x1010004, 0x10404, 4, 0x10000, 0x400, 0x1010400, 0x1010404, 0x400,
              0x1000404, 0x1010004, 0x1000000, 4, 0x404, 0x1000400, 0x1000400, 0x10400, 0x10400, 0x1010000, 0x1010000,
              0x1000404, 0x10004, 0x1000004, 0x1000004, 0x10004, 0, 0x404, 0x10404, 0x1000000, 0x10000, 0x1010404, 4,
              0x1010000, 0x1010400, 0x1000000, 0x1000000, 0x400, 0x1010004, 0x10000, 0x10400, 0x1000004, 0x400, 4,
              0x1000404, 0x10404, 0x1010404, 0x10004, 0x1010000, 0x1000404, 0x1000004, 0x404, 0x10404, 0x1010400, 0x404,
              0x1000400, 0x1000400, 0, 0x10004, 0x10400, 0, 0x1010004]
DES_SPBOX2 = [0x80108020, 0x80008000, 0x8000, 0x108020, 0x100000, 0x20, 0x80100020, 0x80008020, 0x80000020, 0x80108020,
              0x80108000, 0x80000000, 0x80008000, 0x100000, 0x20, 0x80100020, 0x108000, 0x100020, 0x80008020, 0,
              0x80000000, 0x8000, 0x108020, 0x80100000, 0x100020, 0x80000020, 0, 0x108000, 0x8020, 0x80108000,
              0x80100000, 0x8020, 0, 0x108020, 0x80100020, 0x100000, 0x80008020, 0x80100000, 0x80108000, 0x8000,
              0x80100000, 0x80008000, 0x20, 0x80108020, 0x108020, 0x20, 0x8000, 0x80000000, 0x8020, 0x80108000,
              0x100000, 0x80000020, 0x100020, 0x80008020, 0x80000020, 0x100020, 0x108000, 0, 0x80008000, 0x8020,
              0x80000000, 0x80100020, 0x80108020, 0x108000]
DES_SPBOX3 = [520, 0x8020200, 0, 0x8020008, 0x8000200, 0, 0x20208, 0x8000200, 0x20008, 0x8000008, 0x8000008, 0x20000,
              0x8020208, 0x20008, 0x8020000, 520, 0x8000000, 8, 0x8020200, 0x200, 0x20200, 0x8020000, 0x8020008,
              0x20208, 0x8000208, 0x20200, 0x20000, 0x8000208, 8, 0x8020208, 0x200, 0x8000000, 0x8020200, 0x8000000,
              0x20008, 520, 0x20000, 0x8020200, 0x8000200, 0, 0x200, 0x20008, 0x8020208, 0x8000200, 0x8000008, 0x200, 0,
              0x8020008, 0x8000208, 0x20000, 0x8000000, 0x8020208, 8, 0x20208, 0x20200, 0x8000008, 0x8020000, 0x8000208,
              520, 0x8020000, 0x20208, 8, 0x8020008, 0x20200]
DES_SPBOX4 = [0x802001, 0x2081, 0x2081, 0x80, 0x802080, 0x800081, 0x800001, 0x2001, 0, 0x802000, 0x802000, 0x802081,
              0x81, 0, 0x800080, 0x800001, 1, 0x2000, 0x800000, 0x802001, 0x80, 0x800000, 0x2001, 0x2080, 0x800081, 1,
              0x2080, 0x800080, 0x2000, 0x802080, 0x802081, 0x81, 0x800080, 0x800001, 0x802000, 0x802081, 0x81, 0, 0,
              0x802000, 0x2080, 0x800080, 0x800081, 1, 0x802001, 0x2081, 0x2081, 0x80, 0x802081, 0x81, 1, 0x2000,
              0x800001, 0x2001, 0x802080, 0x800081, 0x2001, 0x2080, 0x800000, 0x802001, 0x80, 0x800000, 0x2000,
              0x802080]
DES_SPBOX5 = [0x100, 0x2080100, 0x2080000, 0x42000100, 0x80000, 0x100, 0x40000000, 0x2080000, 0x40080100, 0x80000,
              0x2000100, 0x40080100, 0x42000100, 0x42080000, 0x80100, 0x40000000, 0x2000000, 0x40080000, 0x40080000, 0,
              0x40000100, 0x42080100, 0x42080100, 0x2000100, 0x42080000, 0x40000100, 0, 0x42000000, 0x2080100,
              0x2000000, 0x42000000, 0x80100, 0x80000, 0x42000100, 0x100, 0x2000000, 0x40000000, 0x2080000, 0x42000100,
              0x40080100, 0x2000100, 0x40000000, 0x42080000, 0x2080100, 0x40080100, 0x100, 0x2000000, 0x42080000,
              0x42080100, 0x80100, 0x42000000, 0x42080100, 0x2080000, 0, 0x40080000, 0x42000000, 0x80100, 0x2000100,
              0x40000100, 0x80000, 0, 0x40080000, 0x2080100, 0x40000100]
DES_SPBOX6 = [0x20000010, 0x20400000, 0x4000, 0x20404010, 0x20400000, 16, 0x20404010, 0x400000, 0x20004000, 0x404010,
              0x400000, 0x20000010, 0x400010, 0x20004000, 0x20000000, 0x4010, 0, 0x400010, 0x20004010, 0x4000, 0x404000,
              0x20004010, 16, 0x20400010, 0x20400010, 0, 0x404010, 0x20404000, 0x4010, 0x404000, 0x20404000, 0x20000000,
              0x20004000, 16, 0x20400010, 0x404000, 0x20404010, 0x400000, 0x4010, 0x20000010, 0x400000, 0x20004000,
              0x20000000, 0x4010, 0x20000010, 0x20404010, 0x404000, 0x20400000, 0x404010, 0x20404000, 0, 0x20400010, 16,
              0x4000, 0x20400000, 0x404010, 0x4000, 0x400010, 0x20004010, 0, 0x20404000, 0x20000000, 0x400010,
              0x20004010]
DES_SPBOX7 = [0x200000, 0x4200002, 0x4000802, 0, 0x800, 0x4000802, 0x200802, 0x4200800, 0x4200802, 0x200000, 0,
              0x4000002, 2, 0x4000000, 0x4200002, 2050, 0x4000800, 0x200802, 0x200002, 0x4000800, 0x4000002, 0x4200000,
              0x4200800, 0x200002, 0x4200000, 0x800, 2050, 0x4200802, 0x200800, 2, 0x4000000, 0x200800, 0x4000000,
              0x200800, 0x200000, 0x4000802, 0x4000802, 0x4200002, 0x4200002, 2, 0x200002, 0x4000000, 0x4000800,
              0x200000, 0x4200800, 2050, 0x200802, 0x4200800, 2050, 0x4000002, 0x4200802, 0x4200000, 0x200800, 0, 2,
              0x4200802, 0, 0x200802, 0x4200000, 0x800, 0x4000002, 0x4000800, 0x800, 0x200002]
DES_SPBOX8 = [0x10001040, 0x1000, 0x40000, 0x10041040, 0x10000000, 0x10001040, 0x40, 0x10000000, 0x40040, 0x10040000,
              0x10041040, 0x41000, 0x10041000, 0x41040, 0x1000, 0x40, 0x10040000, 0x10000040, 0x10001000, 0x1040,
              0x41000, 0x40040, 0x10040040, 0x10041000, 0x1040, 0, 0, 0x10040040, 0x10000040, 0x10001000, 0x41040,
              0x40000, 0x41040, 0x40000, 0x10041000, 0x1000, 0x40, 0x10040040, 0x1000, 0x41040, 0x10001000, 0x40,
              0x10000040, 0x10040000, 0x10040040, 0x10000000, 0x40000, 0x10001040, 0, 0x10041040, 0x40040, 0x10000040,
              0x10040000, 0x10001000, 0x10001040, 0, 0x10041040, 0x41000, 0x41000, 0x1040, 0x1040, 0x40040, 0x10000000,
              0x10041000]


class DES:
    n = False
    o = [0] * 64
    p = [0] * 64
    r = [0] * 32
    s = [0] * 32
    t = [0] * 32

    def SHR(self, a, b):
        return (a & 0xFFFFFFFF) >> (b & 255)

    def des_a(self, plain_1, len_plain):
        v0 = [0] * 2
        self.des_b(plain_1, len_plain, v0)
        self.des_c(v0, self.r)
        self.des_c(v0, self.s)
        self.des_c(v0, self.t)
        return self.des_e(v0)

    def des_b(self, arg5, arg6, arg7):
        arg7[0] = (arg5[arg6] & 0xFF) << 24
        arg7[0] |= (arg5[arg6 + 1] & 0xFF) << 16
        arg7[0] |= (arg5[arg6 + 2] & 0xFF) << 8
        arg7[0] |= arg5[arg6 + 3] & 0xFF
        arg7[1] = (arg5[arg6 + 4] & 0xFF) << 24
        arg7[1] |= (arg5[arg6 + 5] & 0xFF) << 16
        arg7[1] |= (arg5[arg6 + 6] & 0xFF) << 8
        arg7[1] |= arg5[arg6 + 7] & 0xFF

    def des_c(self, arg14, arg15):
        v12 = 0xFF00FF
        v11 = 0xFFFF
        v9 = 0xAAAAAAAA
        v0 = arg14[0]
        v3 = (self.SHR(v0, 4) ^ arg14[1]) & 0xF0F0F0F
        v2 = arg14[1] ^ v3
        v0 ^= v3 << 4
        v3 = (self.SHR(v0, 16) ^ v2) & v11
        v2 ^= v3
        v0 ^= v3 << 16
        v3 = (self.SHR(v2, 2) ^ v0) & 0x33333333
        v0 ^= v3
        v2 ^= v3 << 2
        v3 = (self.SHR(v2, 8) ^ v0) & v12
        v0 ^= v3
        v2 ^= v3 << 8
        v2 = (self.SHR(v2, 0x1F) & 1 | v2 << 1) & -1
        v3 = (v0 ^ v2) & v9
        v4 = v0 ^ v3
        v3 ^= v2
        v4 = (v4 << 1 | self.SHR(v4, 0x1F) & 1) & -1
        v0 = 0
        v2 = 0
        while v0 < 8:
            v5 = (v3 << 28 | self.SHR(v3, 4)) ^ arg15[v2]
            v2 = v2 + 1
            v5 = DES_SPBOX1[self.SHR(v5, 24) & 0x3F] | (
                    DES_SPBOX7[v5 & 0x3F] | DES_SPBOX5[self.SHR(v5, 8) & 0x3F] | DES_SPBOX3[
                self.SHR(v5, 16) & 0x3F])
            v6 = arg15[v2] ^ v3
            v2 = v2 + 1
            v4 ^= v5 | DES_SPBOX8[v6 & 0x3F] | DES_SPBOX6[self.SHR(v6, 8) & 0x3F] | DES_SPBOX4[
                self.SHR(v6, 16) & 0x3F] | DES_SPBOX2[self.SHR(v6, 24) & 0x3F]
            v5 = (v4 << 28 | self.SHR(v4, 4)) ^ arg15[v2]
            v2 = v2 + 1
            v5 = DES_SPBOX1[self.SHR(v5, 24) & 0x3F] | (
                    DES_SPBOX7[v5 & 0x3F] | DES_SPBOX5[self.SHR(v5, 8) & 0x3F] | DES_SPBOX3[
                self.SHR(v5, 16) & 0x3F])
            v6 = arg15[v2] ^ v4
            v2 = v2 + 1
            v3 ^= v5 | DES_SPBOX8[v6 & 0x3F] | DES_SPBOX6[self.SHR(v6, 8) & 0x3F] | DES_SPBOX4[
                self.SHR(v6, 16) & 0x3F] | DES_SPBOX2[self.SHR(v6, 24) & 0x3F]
            v0 = v0 + 1
        v0 = v3 << 0x1F | self.SHR(v3, 1)
        v2 = (v4 ^ v0) & v9
        v3 = v4 ^ v2
        v0 ^= v2
        v2 = v3 << 0x1F | self.SHR(v3, 1)
        v3 = (self.SHR(v2, 8) ^ v0) & v12
        v0 ^= v3
        v2 ^= v3 << 8
        v3 = (self.SHR(v2, 2) ^ v0) & 0x33333333
        v0 ^= v3
        v2 ^= v3 << 2
        v3 = (self.SHR(v0, 16) ^ v2) & v11
        v2 ^= v3
        v0 ^= v3 << 16
        v3 = (self.SHR(v0, 4) ^ v2) & 0xF0F0F0F
        arg14[0] = (v0 ^ v3 << 4) & 0xffffffff
        arg14[1] = (v2 ^ v3) & 0xffffffff

    def des_e(self, arg5):
        arg6 = b''
        arg6 += int.to_bytes(self.SHR(arg5[0], 24) & 0xFF, 1, byteorder='little', signed=False)
        arg6 += int.to_bytes(self.SHR(arg5[0], 16) & 0xFF, 1, byteorder='little', signed=False)
        arg6 += int.to_bytes(self.SHR(arg5[0], 8) & 0xFF, 1, byteorder='little', signed=False)
        arg6 += int.to_bytes(arg5[0] & 0xFF, 1, byteorder='little', signed=False)
        arg6 += int.to_bytes(self.SHR(arg5[1], 24) & 0xFF, 1, byteorder='little', signed=False)
        arg6 += int.to_bytes(self.SHR(arg5[1], 16) & 0xFF, 1, byteorder='little', signed=False)
        arg6 += int.to_bytes(self.SHR(arg5[1], 8) & 0xFF, 1, byteorder='little', signed=False)
        arg6 += int.to_bytes(arg5[1] & 0xFF, 1, byteorder='little', signed=False)
        return arg6

    def des_d(self, param):
        param[0:32] = self.r[0:]

    def des_f(self, arg2, arg3):
        if self.n:
            return self.des_a(arg2, arg3)

    def des_g(self, param):
        self.r[0:] = param[0:32]
        self.n = False

    def des_h(self, param):
        self.des_d(param)
        param[32:] = self.s[0:]

    def des_i(self, param):
        self.des_g(param)
        self.s[0:] = param[32:]
        self.des_d(self.t)
        self.n = True

    def des_set_key_8(self, arg10, arg11):
        v3 = [True] * 56
        v4 = [True] * 56

        for v1 in range(56):
            v0 = True if (arg10[self.SHR(key_table[v1], 3)] & bitTable[key_table[v1] & 7]) != 0 else False
            v3[v1] = v0

        for v1 in range(16):
            v0_1 = 15 - v1 << 1 if not arg11 else v1 << 1
            v5 = v0_1 + 1
            self.r[v5] = 0
            self.r[v0_1] = 0

            for v2 in range(28):
                v6 = left_shift_table[v1] + v2
                v4[v2] = v3[v6] if v6 < 28 else v3[v6 - 28]

            for v2 in range(28, 56):
                v6 = left_shift_table[v1] + v2
                v4[v2] = v3[v6] if v6 < 56 else v3[v6 - 28]

            for v2 in range(24):
                if v4[after_shift_table[v2]]:
                    self.r[v0_1] |= bigbyte[v2]
                if v4[after_shift_table[v2 + 24]]:
                    self.r[v5] |= bigbyte[v2]

        for v0_1 in range(0, 32, 2):
            v1 = self.r[v0_1]
            v2 = self.r[v0_1 + 1]
            self.r[v0_1] = (0xFC0000 & v1) << 6 | (v1 & 0xFC0) << 10 | (0xFC0000 & v2) >> 10 | (v2 & 0xFC0) >> 6
            self.r[v0_1 + 1] = (v1 & 0x3F) << 16 | (0x3F000 & v1) << 12 | (0x3F000 & v2) >> 4 | v2 & 0x3F

        self.n = False

    def des_set_key_16(self, key, opType):
        self.des_set_key_8(key[8:], not opType)
        self.des_d(self.s)
        self.des_set_key_8(key[0:8], opType)
        self.des_d(self.t)
        self.n = True

    def setKey(self, key, opType):
        keyLength = len(key)
        if keyLength != 16 and keyLength != 8:
            return False
        if keyLength == 16:
            self.des_set_key_16(key, opType)
        else:
            self.des_set_key_8(key, opType)
        return True

    def operate(self, plain, opType):
        cipher_text = b''
        if len(plain) == 0:
            return

        if opType:
            self.des_i(self.o)
        else:
            self.des_i(self.p)

        v1 = len(plain) // 8
        for v0 in range(v1):
            v2 = v0 * 8
            cipher_text += self.des_f(plain, v2)
        return cipher_text

    def __init__(self, key):
        self.setKey(key, True)
        self.des_h(self.o)
        self.setKey(key, False)
        self.des_h(self.p)
        pass


def des(data, des_key, opType):
    des_op = DES(des_key)
    return des_op.operate(data, opType)

