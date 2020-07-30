from StuffStructStream import StuffStructStream
from StuffTableStruct import StuffTableStruct
import json


class fth:
    a = 0x80000000
    b = 0xFFFFFFFF
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0

    def d_m(self):
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0
        self.g = 0

    def c_m(self):
        if self.g == -2147483648 or self.g == -1 or self.g == self.a or self.g == self.b:
            return True
        return False

    def a_m(self):
        return 0 if self.f == 0 else self.e

    def a_long(self, arg4):
        if arg4 == 0:
            self.d_m()
        self.g = arg4
        self.c = int(0x7FFFFFF & arg4)
        self.d = int((0x8000000 & arg4) >> 27)
        self.e = int((0x70000000 & arg4) >> 28)
        self.f = int((-2147483648 & arg4) >> 0x1F)

    def e_m(self):
        return False if self.c != 0 or self.d != 0 or self.e != 0 or self.f != 0 else True

    def b_m(self):
        if self.c_m():
            v0 = -2147483648
        elif self.e_m():
            v0 = 0
        else:
            v0 = pow(10, self.e)
            if self.f == 1:
                v0 = self.c / v0
            else:
                v0 *= self.c
            if self.d != 0:
                v0 = -v0
        return v0


def handle_case_0(data_header, decode_Data):
    if decode_Data.available() < 24:
        return ''

    v2_1 = True if data_header.id != -1 else False
    type_str = str(decode_Data.readBytesOnly(6), encoding='gbk')

    if type_str[0:2] == '8,':
        data = decode_Data.readBytes(decode_Data.available())
        return str(data, encoding='gbk')

    if type_str[0:2] != 'tb' and type_str[0:2] != 'cv':
        return ''

    sss = StuffStructStream()
    decode_Data = sss.d(decode_Data)
    if type_str[0:2] == 'tb':
        sts = StuffTableStruct(v2_1)
        title = decode_Data.readUTF()
        sts.caption = title
        v4 = readTableExtData(sss, decode_Data, sts)
        readTableData(sss, decode_Data, sts, v4)
        json_data = json.dumps(v4)
        return json_data

    # cv的数据暂未处理
    return 'this is a stuffCurveData, no decoding'


def readTableExtData(sss, decode_Data, sts):
    v3 = sss.i
    v4 = []
    # 读取扩展数据
    if sss.e > v3 - decode_Data.available():
        v0 = 0
        # 此处v2和v5似乎没什么用, 先屏蔽掉再说
        # v2 = 0
        # v5 = []
        while v0 < sss.g:
            v6 = decode_Data.readUTF()
            if v6 != "":
                # v2 = 1
                v4.append(v6)
            # v5.append(sss.h[v0].a & 0x8FFF)
            v0 += 1
        '''
        if v2 != 0:
            sts.tableHead = v4
            sts.n = v5
        '''
        v4 = {'TableHeader': v4}
    if sss.e > v3 - decode_Data.available():
        v4_1 = decode_Data.readShort()
        if 0 <= v4_1 <= 100:
            v5_1 = {}
            v6_1 = sts.r
            for v2 in range(v4_1):
                v7 = decode_Data.readUnsignedShort()
                v8 = v7 & 0x8FFF
                mark = v7 & 0x7000
                if mark == 0:
                    v0_1 = decode_Data.readUTF()
                    if v0_1 != "":
                        v5_1[v8] = v0_1
                    else:
                        break
                elif mark == 0x2000:
                    v5_1[v8] = decode_Data.readInt()
                elif mark == 0x6000:
                    if v8 == 0x8008:
                        v9 = decode_Data.readShort()
                        if v9 > 0:
                            v10 = []
                            for v0 in range(v9):
                                v10.append(decode_Data.readInt())
                            v5_1[v8] = v10
                v6_1[v8] = v7
            sts.q = v5_1
            v0 = v3 - decode_Data.available()
            if sss.e > v0:
                decode_Data.skipBytes(sss.e - v0)
    else:
        v0 = v3 - decode_Data.available()
        if sss.e > v0:
            decode_Data.skipBytes(sss.e - v0)

    if not v4:
        v4 = {'TableHeader': []}
    return v4


def readTableData(sss, decode_Data, sts, json_data):
    v2 = 0
    v11 = 0x8008 in sts.r if sts.r != {} else False
    if v11:
        v2 = False if sts.q == {} else sts.q[0x8008]
        if v2:
            v8 = v2
            v9 = sss.c
            v10 = sss.g
    else:
        v8 = v2
        v9 = sss.g
        v10 = sss.b
    if v10 > 0 and v9 > 0:
        # v12 = {}
        # v13 = {}
        # v14 = sts.r
        v15 = fth()
        # row
        TableDatas = []
        for v7 in range(v10):
            # column
            TableData = []
            for v6 in range(v9):
                v16 = ''
                if v11:
                    v3 = v8[v6]
                    v4 = sss.h[v7].a | v3
                else:
                    v4 = sss.h[v6].a
                    v3 = 0x8FFF & v4

                '''
                v5 = v3
                if v7 == 0:
                    v2_2 = []
                    v3_1 = []
                    v14[v5] = v4
                    v12[v5] = v2_2
                    v13[v5] = v3_1
                    TableData = v2_2
                else:
                    v2 = v12[v5]
                    v3_2 = v13[v5]
                    v5_2 = v2
                '''

                if v4 & 0x7000 == 0:
                    v2_1 = int(sss.h[v7].b / 2 if v11 else sss.h[v6].b / 2)
                    v4_1 = decode_Data.readUnicode2UTF8(v2_1)
                    v2_1 = decode_Data.readByte()
                    if v4_1 != '':
                        v16 += v4_1
                        v16 = eus_a_i_s(v2_1, v16)
                elif v4 & 0x7000 == 4096:
                    arg4 = decode_Data.readLong()
                    v15.a_long(arg4)
                    v2_1 = decode_Data.readByte()
                    v16 = eus_a_fth_i_s(v15, v2_1, v16)
                elif v4 & 0x7000 == 8192:
                    v4 = str(decode_Data.readInt())
                    v2_1 = decode_Data.readByte()
                    v16 += v4
                    v16 = eus_a_i_s(v2_1, v16)
                elif v4 & 0x7000 == 1288:
                    v4 = str(decode_Data.readShort())
                    v2_1 = decode_Data.readByte()
                    v16 += v4
                    v16 = eus_a_i_s(v2_1, v16)
                TableData.append(v16.strip())
                # fse_a = [0xFF000000, 0xFF00A8A8, 0xFF00FF00, 0xFF00FFFF, 0xFF5454FF, 0xFF54FF54, 0xFF54FFFF, 0xFFA80000,
                #         0xFFA8A8A8, 0xFFC8C8C8, 0xFFFF0000, 0xFFFF5454, 0xFFFF54FF, 0xFFFFFF00, 0xFFFFFF54, -1]
                # v3_1.append(0 if (v2_1 & 15) < 0 or (v2_1 & 15) >= len(fse_a) else fse_a[v2_1 & 15])
            TableDatas.append(TableData)
        json_data['TableData'] = TableDatas
        sts.s = v10
        sts.t = v9
        # sts.o = v12
        # sts.p = v13


def fse_a_i(arg1):
    if arg1 == 16:
        return '万手'
    elif arg1 == 0x20:
        return '%'
    elif arg1 == 0x30:
        return '亿'
    elif arg1 == 0x40:
        return '万'
    elif arg1 == 0:
        return ''


def eus_a_i_s(arg1, arg2):
    v0 = fse_a_i(arg1 & 0xF0)
    if v0 != '':
        return arg2 + v0
    return arg2


def eus_a_fth_i_s(arg4, arg5, arg6):
    if arg4.c_m():
        return arg6 + '--'
    else:
        arg6 = fti_a(arg4.b_m(), arg4.a_m(), True)
        arg6 = eus_a_i_s(arg5, arg6)
        return arg6


def fti_a(arg10, arg12, arg13):
    fti_a = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]
    v9 = '.'
    v8 = '0'
    v0 = 0.5
    v2 = 0
    v4 = 0
    arg14 = ''
    if 0 <= arg12 < len(fti_a):
        if arg10 != v2:
            if arg12 == 0:
                if not arg13:
                    v0 = arg10
                elif arg10 > v2:
                    v0 += arg10
                else:
                    v0 = arg10 - v0
                arg14 += str(v0)
            else:
                if arg12 <= 0:
                    return arg14
                if arg10 < v2:
                    v5 = 1
                    arg10 = -arg10
                else:
                    v5 = 0
                if not arg13:
                    v0 = v2
                v0_1 = v0 + fti_a[arg12] * arg10
                arg14 += str(v0_1)
                v0 = v0_1 / fti_a[arg12]
                if v0 < 1:
                    if v0 < 0.1:
                        v1 = arg12 - len(arg14)
                        for _ in range(v1):
                            arg14 = v8 + arg14
                    arg14 = '0.' + arg14
                else:
                    if len(arg14) - arg12 >= 0:
                        arg14 = arg14[0:len(arg14) - arg12] + str(v9) + arg14[len(arg14) - arg12:]
                if v5 == 0:
                    return arg14
                arg14 = '-' + arg14
            return arg14
        arg14 += v8
        if arg12 <= 0:
            return arg14
        arg14 += v9
        while v4 < arg12:
            arg14 += v8
            v4 += 1
        return arg14
    return arg14

