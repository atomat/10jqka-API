#  不要问这部分干嘛的
#  我也看不懂, 差点儿就疯了
#  这部分代码debug了两整天...


def from_bytes(p, v):
    return int.from_bytes(bytes(p[v: v + 1]), byteorder='little')


def to_bytes(p, v, index):
    p[index: index + 1] = bytearray(int.to_bytes(v, 1, byteorder='little', signed=False))


def ftj_b(p0_bytes, p1, p2, p3_bytes, p4):
    p0 = bytearray(p0_bytes)
    p3 = bytearray(p3_bytes)
    v4 = 8
    v5 = 0
    v2 = p1 + 1
    v1 = from_bytes(p0, p1)
    v0 = 1
    v3 = v2 + 1
    v2 = from_bytes(p0, v2)
    to_bytes(p3, v2, v5)
    v7 = v4
    v6 = v3
    v3 = v0
    v0 = v2
    while v3 < p4:
        v8 = v1 & 0x80
        v1 += v1
        v2 = v1
        v1 = v7 - 1
        if v1 != 0:
            v5 = v6
        else:
            v5 = v6 + 1
            v1 = from_bytes(p0, v6)
            v2 = v1
            v1 = v4
        if v8 != 0:
            v7 = v2 & 0x80
            v2 += v2
            v1 -= 1
            if v1 != 0:
                v6 = v2
                v9 = v1
                v1 = v5
                v5 = v9
            else:
                v2 = v5 + 1
                v1 = from_bytes(p0, v5)
                v5 = v4
                v6 = v1
                v1 = v2
            if v7 != 0:
                v2 = v0
                v0 = v1
                v1 = v3
            else:
                v2 = v3 + 1
                v0 = v1 + 1
                v1 = from_bytes(p0, v1)
                to_bytes(p3, v1, v3)
                v9 = v2
                v2 = v1
                v1 = v9
            v7 = v1 + 1
            to_bytes(p3, v2, v1)
            v8 = v6 & 0x80
            v1 = v6 + v6
            v3 = v1
            v1 = v5 - 1
            if v1 != 0:
                v5 = v0
                v0 = v1
                v1 = v3
            else:
                v5 = v0 + 1
                v0 = from_bytes(p0, v0)
                v1 = v0
                v0 = v4
            if v8 == 0:
                v6 = v5
                v3 = v7
                v7 = v0
                v0 = v2
                continue
            v6 = v7 + 1
            to_bytes(p3, v2, v7)
            v7 = v1 & 0x80
            v1 += v1
            v0 -= 1
            if v0 != 0:
                v3 = v5
            else:
                v3 = v5 + 1
                v0 = from_bytes(p0, v5)
                v1 = v0
                v0 = v4
            if v7 == 0:
                v5 = v1 & 0x80
                v1 += v1
                v0 -= 1
                if v0 == 0:
                    v1 = v3 + 1
                    v0 = from_bytes(p0, v3)
                    v3 = v1
                    v1 = v0
                    v0 = v4
                if v5 == 0:
                    v7 = v0
                    v0 = v2
                    v9 = v6
                    v6 = v3
                    v3 = v9
                    continue
                v5 = v6 + 1
                to_bytes(p3, v2, v6)
                v7 = v0
                v6 = v3
                v3 = v5
                v0 = v2
                continue
            v7 = v6 + 1
            to_bytes(p3, v2, v6)
            v5 = v7 + 1
            to_bytes(p3, v2, v7)
            v6 = v1 & 0x80
            v1 += v1
            v0 -= 1
            if v0 == 0:
                v1 = v3 + 1
                v0 = from_bytes(p0, v3)
                v3 = v1
                v1 = v0
                v0 = v4
            if v6 == 0:
                v7 = v0
                v6 = v3
                v3 = v5
                v0 = v2
                continue
            v6 = v5 + 1
            to_bytes(p3, v2, v5)
            v7 = v1 & 0x80
            v1 += v1
            v0 -= 1
            if v0 != 0:
                v5 = v3
            else:
                v5 = v3 + 1
                v0 = from_bytes(p0, v3)
                v1 = v0
                v0 = v4
            if v7 == 0:
                v7 = v1 & 0x80
                v1 += v1
                v0 -= 1
                if v0 != 0:
                    v3 = v5
                else:
                    v3 = v5 + 1
                    v0 = from_bytes(p0, v5)
                    v1 = v0
                    v0 = v4
                if v7 == 0:
                    v5 = v1 & 0x80
                    v1 += v1
                    v0 -= 1
                    if v0 == 0:
                        v1 = v3 + 1
                        v0 = from_bytes(p0, v3)
                        v3 = v1
                        v1 = v0
                        v0 = v4
                    if v5 == 0:
                        v7 = v0
                        v0 = v2
                        v9 = v6
                        v6 = v3
                        v3 = v9
                        continue
                    v5 = v6 + 1
                    to_bytes(p3, v2, v6)
                    v7 = v0
                    v6 = v3
                    v3 = v5
                    v0 = v2
                    continue
                v5 = v1 & 0x80
                v1 += v1
                v0 -= 1
                if v0 == 0:
                    v1 = v3 + 1
                    v0 = from_bytes(p0, v3)
                    v3 = v1
                    v1 = v0
                    v0 = v4
                if v5 == 0:
                    v7 = v6 + 1
                    to_bytes(p3, v2, v6)
                    v5 = v7 + 1
                    to_bytes(p3, v2, v7)
                    v7 = v0
                    v6 = v3
                    v3 = v5
                    v0 = v2
                    continue
                v5 = v6 + 1
                to_bytes(p3, v2, v6)
                v6 = v5 + 1
                to_bytes(p3, v2, v5)
                v5 = v6 + 1
                to_bytes(p3, v2, v6)
                v7 = v0
                v6 = v3
                v3 = v5
                v0 = v2
                continue
            v3 = v6 + 1
            to_bytes(p3, v2, v6)
            v6 = v3 + 1
            to_bytes(p3, v2, v3)
            v3 = v6 + 1
            to_bytes(p3, v2, v6)
            v6 = v3 + 1
            to_bytes(p3, v2, v3)
            v7 = v1 & 0x80
            v1 += v1
            v0 -= 1
            if v0 != 0:
                v3 = v5
            else:
                v3 = v5 + 1
                v0 = from_bytes(p0, v5)
                v1 = v0
                v0 = v4
            if v7 == 0:
                v5 = v1 & 0x80
                v1 += v1
                v0 -= 1
                if v0 == 0:
                    v1 = v3 + 1
                    v0 = from_bytes(p0, v3)
                    v3 = v1
                    v1 = v0
                    v0 = v4
                if v5 == 0:
                    v7 = v0
                    v0 = v2
                    v9 = v6
                    v6 = v3
                    v3 = v9
                    continue
                v5 = v6 + 1
                to_bytes(p3, v2, v6)
                v7 = v0
                v6 = v3
                v3 = v5
                v0 = v2
                continue
            v5 = v1 & 0x80
            v1 += v1
            v0 -= 1
            if v0 != 0:
                v7 = v0
                v8 = v1
                v0 = v3
            else:
                v1 = v3 + 1
                v0 = from_bytes(p0, v3)
                v7 = v4
                v8 = v0
                v0 = v1
            if v5 == 0:
                v1 = v6 + 1
                to_bytes(p3, v2, v6)
                v3 = v1 + 1
                to_bytes(p3, v2, v1)
                v1 = v8
                v6 = v0
                v0 = v2
                continue
            v1 = v6 + 1
            to_bytes(p3, v2, v6)
            v3 = v1 + 1
            to_bytes(p3, v2, v1)
            v1 = v3 + 1
            to_bytes(p3, v2, v3)
            v5 = v0 + 1
            v0 = from_bytes(p0, v0)
            if v0 >= 0:
                v3 = v0
            else:
                v3 = 0x100
                v0 += v3
                v3 = v0
            v6 = 0x7f
            if v3 <= v6:
                v6 = v3
                v3 = v0
                v0 = v5
            else:
                v0 = v3 - 0x80
                v0 = v0 << 8
                v3 = v5 + 1
                v5 = from_bytes(p0, v5)
                if v5 < 0:
                    v0 += 0x100
                v0 += v5
                v6 = v0
                v9 = v3
                v3 = v0
                v0 = v9
            while True:
                v5 = v3 - 1
                if v3 == 0:
                    v3 = 0x7fff
                    if v6 == v3:
                        v5 = v0 + 1
                        v0 = from_bytes(p0, v0)
                        if v0 >= 0:
                            v3 = v0
                        else:
                            v3 = 0x100
                            v0 += v3
                            v3 = v0
                        v6 = 0x7f
                        if v3 <= v6:
                            v6 = v3
                            v3 = v0
                            v0 = v5
                            continue
                        v0 = v3 - 0x80
                        v0 = v0 << 8
                        v3 = v5 + 1
                        v5 = from_bytes(p0, v5)
                        if v5 < 0:
                            v0 += 0x100
                        v0 += v5
                        v6 = v0
                        v9 = v3
                        v3 = v0
                        v0 = v9
                        continue
                    v6 = v0
                    v3 = v1
                    v1 = v8
                    v0 = v2
                    continue
                v3 = v1 + 1
                to_bytes(p3, v2, v1)
                v1 = v3
                v3 = v5
        else:
            v6 = v3 + 1
            v7 = v5 + 1
            v0 = from_bytes(p0, v5)
            to_bytes(p3, v0, v3)
            v0 = v6 + 1
            v3 = v7 + 1
            v5 = from_bytes(p0, v7)
            to_bytes(p3, v5, v6)
            v7 = v1
            v6 = v3
            v1 = v2
            v3 = v0
            v0 = v5
            continue
    return p4, bytes(p0), bytes(p3)


