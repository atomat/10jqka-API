import random


def luhn_residue(digits):
    return sum(sum(divmod(int( d) * (1 + i % 2), 10))
               for i, d in enumerate(digits[::-1])) % 10


def getImei():
    part = ''.join(str(random.randrange(0, 9)) for _ in range(14))
    res = luhn_residue('{}{}'.format(part, 0))
    return '{}{}'.format(part, -res % 10)


def getMac():
    mac = ''
    for _ in range(6):
        mac += int.to_bytes(random.randint(0, 255), 1, byteorder='little', signed=False).hex() + ':'
    return mac[:-1]
