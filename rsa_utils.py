import constants

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from rsa import transform, core


# 常见的rsa加密
def rsa_encrypt(data):
    rsakey = RSA.importKey(constants.RSA_KEY)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    return cipher.encrypt(data)


# 上述rsa加密不支持不标准的密钥, 采用下面的方法对数据包加密密钥进行加密/解密
def rsa_encrypt_key(data):
    data = transform.bytes2int(data)
    encrypted = core.encrypt_int(data, constants.RSA_E, constants.RSA_N)
    print(constants.RSA_N)
    block = transform.int2bytes(encrypted, 64)
    return block