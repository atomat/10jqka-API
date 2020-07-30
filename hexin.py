# 同花顺安卓端交易协议
import json
import os
import random
import sys
from socket import *
import base64
from urllib import parse

import snappy

import requests

import Des
import constants
import rsa_utils
import dataHelper
from header import MiniDataHead
from OutputStream import OutputStream
from stuffTextData import stuffTextData
from stuffInteractData import stuffInteractData


# 处理未定义情况的数据包, 比如接收到不是发送包id的数据包时, 由该部分完成处理
# 相当于同步情况下的异步吧, 想要速度的话, 这部分可以扔在线程里面, 或者收到包就先解析id, 不符合条件的扔到线程中
def default_handle_data(ret_data):
    if constants.log == 1:
        print(ret_data)


# 处理接收到的数据,负责完成数据解压缩/数据解密/数据解析/数据分发等工作
def handle_data(data):

    if len(data) < 24:
        return

    decode_Data = OutputStream(data)

    data_header = MiniDataHead(decode_Data.readBytes(24))

    if data_header.id == 8888:
        data_header.type |= 0x0A

    # 加密种类
    enc_type = data_header.type & 0xF0000000

    # 数据包被DES加密
    if enc_type == 0x10000000:
        plain_data = Des.des(decode_Data.readBytes(decode_Data.available()), globals()['server_key'], False)
        decode_Data.__init__(plain_data)

    # 数据包被RSA_短密钥加密,这种情况暂时未遇到,不能上线正式环境,如果出现,尝试解密后抛出异常以便分析
    if enc_type == 0x20000000:
        if constants.debug == 1:
            assert False, 'RSA!!!'

    # 数据包被AES加密,这种情况暂时未遇到,不能上线正式环境,如果出现,抛出异常以便分析
    if enc_type == 0x70000000:
        if constants.debug == 1:
            assert False, 'AES!!!'

    # 数据包被压缩
    if data_header.type & 0xF000 == 0x1000:
        uncompress_data = snappy.uncompress(decode_Data.readBytes(data_header.pageId))
        data = uncompress_data + decode_Data.readBytes(decode_Data.available())
        decode_Data.__init__(data)

    # 进程数据各类情况,暂时未遇到,先直接无视,以后有时间再完善
    if data_header.id == -3:
        if constants.debug == 1:
            if data_header.type & 15 == 11:
                assert False, 'data_header.id == -3'

    mark = data_header.type & 15  # 采用字典代替switch

    if constants.log == 1:
        print('data_mark={}'.format(mark))

    ret_data = ''

    # 主要包含StuffCurveStruct以及StuffTableStruct两种格式数据的处理
    # StuffCurveStruct应该包含的是股票的详细信息, 这部分暂未完成解析, 感觉用处不大
    # StuffTableStruct包含了除股票信息之类, 比如个人持仓之类的信息
    def case_0():
        nonlocal ret_data
        ret_data = dataHelper.handle_case_0(data_header, decode_Data)

    # 系统消息
    def case_1():
        nonlocal ret_data
        stuffTextData_data = stuffTextData(data_header.type, decode_Data.readBytes(decode_Data.available()))
        ret_data = stuffTextData_data.title + ':' + stuffTextData_data.content

    def case_3():
        nonlocal ret_data
        number = decode_Data.readByte()
        decode_Data.skipBytes(1)
        for _ in range(number):
            dataId = decode_Data.readUnsignedShort()
            ctrlType = decode_Data.readInt()
            colorIndex = decode_Data.readByte()
            content = decode_Data.readUTF()
            ret_data += 'stuffCtrlData:' + 'dataId=' + str(dataId) + ',ctrlType=' + str(ctrlType) + ',colorIndex=' + str(
                colorIndex) + ',content=' + content + '\n'

    # 券商登录成功返回
    def case_4():
        nonlocal ret_data
        if data_header.type == 0x10000004:
            ret_data = '证券登录成功'
            return
        if data_header.type == 0x30000004:
            ret_data = '连接中断'
            return
        ret_data = '证券登录失败'

    # 同花顺连接认证以及登录返回
    def case_6():
        nonlocal ret_data
        content_header = decode_Data.readByte()
        if content_header == 128:
            globals()['qs_login_header'] = decode_Data.readBytes(2)
            data_length = decode_Data.readShort()
            # 这部分数据用于二次登录的使用, 手机上的登录保持就是由于该数据.
            if data_length > 0:
                passport_dat = decode_Data.readBytes(data_length)
                # 写出passport.dat内容, 下一次直接加载登录就可以
                passport_dat = b'\x00\x00' + passport_dat[0:2] + passport_dat
                with open("passport.dat", mode='wb') as f:
                    f.write(passport_dat)
            # 以下数据是服务器返回的帐号登录信息
            data_length = decode_Data.readShort()
            if data_length > 0:
                data_bytes = decode_Data.readBytes(data_length)
                data_str = str(data_bytes, encoding='gbk')
                # 判断一下手机号是否已经登录
                if data_str[-4:] != 'sid=':
                    nonlocal ret_data
                    ret_data = '登录成功'
                    return

            ret_data = decode_Data.readUTF()
            if ret_data == "":
                ret_data = '需要手机号登录'


            # 这部分数据没必要解析, 主要包含sessid以及服务器地址和端口等
            '''
            decode_Data.skipBytes(5)
            data_length = decode_Data.readShort()
            if data_length > 0:
                data_bytes = decode_Data.readBytes(data_length)
                data_str = str(data_bytes, encoding='gbk')
                print('server data: ' + data_str)

            decode_Data.skipBytes(2)
            data_length = decode_Data.readShort()
            if data_length > 0:
                data_bytes = decode_Data.readBytes(data_length)
                data_str = str(data_bytes, encoding='gbk')
                print('server data: ' + data_str)

            data_length = decode_Data.readShort()
            if data_length > 0:
                data_bytes = decode_Data.readBytes(data_length)
                data_str = str(data_bytes, encoding='gbk')
                print('server data: ' + data_str)
            '''

    def case_7():
        nonlocal ret_data
        server_data = decode_Data.readBytes(decode_Data.available())
        ret_data = str(server_data, encoding='gbk')
        if constants.debug == 1:
            assert False, 'case_7'

    def case_9():
        nonlocal ret_data
        server_data = decode_Data.readBytes(decode_Data.available())
        ret_data = str(server_data, encoding='gbk')

    # 同花顺或证券登录成功后返回的个人数据或自选
    def case_11():
        nonlocal ret_data
        server_data = decode_Data.readBytes(data_header.pageId)
        ret_data = str(server_data, encoding='gbk')

    def case_13():
        nonlocal ret_data
        stuffInteractData_data = stuffInteractData(decode_Data.readBytes(decode_Data.available()))
        ret_data = stuffInteractData_data.title + ':' + stuffInteractData_data.content

    def case_15():
        nonlocal ret_data
        stuffTextData_data = stuffTextData(data_header.type, decode_Data.readBytes(decode_Data.available()))
        ret_data = stuffTextData_data.title + ':' + stuffTextData_data.content

    def default():
        nonlocal ret_data
        ret_data = "出错"
        if constants.log == 1:
            print('No such case:' + str(mark))

    # python没有switch, 通过这样的方式曲线救国
    switch = {0: case_0,
              1: case_1,
              3: case_3,
              4: case_4,
              6: case_6,
              7: case_7,
              9: case_9,
              11: case_11,
              13: case_13,
              14: case_15,
              15: case_15,
              }
    switch.get(mark, default)()
    return ret_data, data_header.id


# 接收数据工厂,负责完成数据接收/粘包处理工作
# 由于缓存为16*1024,因此暂时不考虑复杂粘包情况,出现的时候再修改吧
def recv_factory(id, *datas):
    for _ in range(30):
        if constants.debug != 1:
            recv_data = tcp_client_socket.recv(constants.BUFFER_CACHE)
        else:
            recv_data = datas[0]
            i = 31
        if constants.log == 1:
            print('recv:' + recv_data.hex(), globals()['server_key'].hex())

        if len(recv_data) <= 12:
            return

        index = recv_data.find(constants.DATA_MARK)
        while index > -1:
            index += 8  # +8是为了跳过data_mark
            length = int(recv_data[index:index + 4], 16)  # 加4为获取一个四字节的int
            if length <= 32:
                break
            index += 5  # 索引跳过一个int和一个00位
            if index + length > len(recv_data):
                break
            data = recv_data[index:index + length]
            ret_data, ret_id = handle_data(data)
            if ret_id == id:
                return ret_data
            default_handle_data(ret_data)
            recv_data = recv_data[index + length:]
            index = recv_data.find(constants.DATA_MARK)
    return ""


# 获取包ID,全局唯一,不可重复,否则掉线,采用自增算法
def get_pack_id():
    global pack_id
    res = pack_id
    pack_id = pack_id + 1
    return res


# 数据包添加一些标志的标头
def add_header(data, data_header, is_encrypt):
    if is_encrypt:
        data = int.to_bytes(data_header.id, 2, byteorder='little', signed=False) + globals()[
            'qs_login_header'] + b'\x00\x00' + data
        # 长度需要为8的倍数
        data = data + b"\x00\x00\x00\x00\x00\x00\x00"
        data = data[0:int(len(data) / 8) * 8]
        data = Des.des(data, server_key, True)

        data_length = len(data) - data_header.textLength
        data_header.dataLength = data_length
        if data_header.type == 0:
            data_header.type = 0x11010000
        if data_header.dataLength == 0:
            data_header.dataLength = len(data)
    else:
        if data_header.type == 0:
            data_header.type = 0x1010000

    if data_header.pageId == 0:
        data_header.pageId = 0xFF00

    full_data = b''
    full_data += int.to_bytes(data_header.headLength, 2, byteorder='little', signed=False)
    full_data += int.to_bytes(data_header.id, 4, byteorder='little', signed=False)
    full_data += int.to_bytes(data_header.type, 4, byteorder='little', signed=False)
    full_data += int.to_bytes(data_header.pageId, 2, byteorder='little', signed=False)
    full_data += int.to_bytes(data_header.dataLength, 4, byteorder='little', signed=False)
    full_data += int.to_bytes(data_header.frameId, 4, byteorder='little', signed=False)
    full_data += int.to_bytes(data_header.textLength, 4, byteorder='little', signed=False)
    full_data += int.to_bytes(data_header.sessionType, 4, byteorder='little', signed=False)
    full_data += data

    data_length = int.to_bytes(len(full_data), 4, byteorder='big').hex().encode()
    data = b'\xfd\xfd\xfd\xfd' + data_length + b'\x00' + full_data
    return data


# 获取券商登录数据包
# 帐号、密码、通信密码（可空）、其他三个券商相关参数
def get_qs_login_data(account, password, txmm, qsid, wtid, dtkltype):
    qssj = wtid + "#" + qsid + "#" + dtkltype + "#1#"
    reqpage = str(random.randint(10000, 99999))

    data = b'\x13\x02\x00\x01\x00\x30\x01\x01\x00\x30'

    data += int.to_bytes(2, 1, byteorder='little', signed=False)
    data += int.to_bytes(len(account), 2, byteorder='little', signed=False)
    data += str.encode(account)

    data += int.to_bytes(3, 1, byteorder='little', signed=False)
    data += int.to_bytes(len(password), 2, byteorder='little', signed=False)
    data += str.encode(password)

    data += int.to_bytes(4, 1, byteorder='little', signed=False)
    data += int.to_bytes(len(txmm), 2, byteorder='little', signed=False)
    data += str.encode(txmm)

    data += int.to_bytes(5, 1, byteorder='little', signed=False)
    data += int.to_bytes(0, 2, byteorder='little', signed=False)

    data += int.to_bytes(6, 1, byteorder='little', signed=False)
    data += int.to_bytes(len(qssj), 2, byteorder='little', signed=False)
    data += str.encode(qssj)

    data += int.to_bytes(7, 1, byteorder='little', signed=False)
    data += int.to_bytes(len(reqpage), 2, byteorder='little', signed=False)
    data += str.encode(reqpage)

    data += int.to_bytes(8, 1, byteorder='little', signed=False)
    data += int.to_bytes(1, 2, byteorder='little', signed=False)
    data += int.to_bytes(49, 1, byteorder='little', signed=False)

    data += int.to_bytes(9, 1, byteorder='little', signed=False)
    HD_INFO = 'HDInfo=' + constants.HD_INFO
    data += int.to_bytes(len(HD_INFO), 2, byteorder='little', signed=False)
    data += str.encode(HD_INFO)

    # 这部分数据直接固定
    data += b'\x0a\x00\x00\x0b\x00\x00\x0c\x00\x00\x0d\x01\x00\x30\x0e\x00\x00\x0f\x00\x00\x10\x00\x00\x11\x00\x00' \
            b'\x12\x00\x00'

    # 主要数据构造完毕,接下来构造包头
    pack_id_temp = get_pack_id()

    data_header = b''
    data_header += int.to_bytes(pack_id_temp, 2, byteorder='little', signed=False)
    data_header += globals()['qs_login_header']
    data_header += int.to_bytes(70024 & 65535, 2, byteorder='little', signed=False)

    # data长度不够8的倍数则用00补齐
    data = data_header + data + b"\x00\x00\x00\x00\x00\x00\x00"

    data = data[0:int(len(data) / 8) * 8]

    data_length = len(data)
    enc_data = Des.des(data, globals()['server_key'], True)
    enc_key = constants.RSA_KEY_HEADER
    enc_key += globals()['qs_login_header']
    enc_key += globals()['server_key']
    enc_key = rsa_utils.rsa_encrypt_key(enc_key)
    enc_key_length = len(enc_key)

    data_header = MiniDataHead()
    data_header.headLength = 28
    data_header.id = pack_id_temp
    data_header.type = 0x11188 | 0x50000000
    data_header.dataLength = data_length  # 加密前以及添加包头前数据的长度
    data_header.frameId = 0xA2A
    data_header.textLength = enc_key_length

    data = b''
    data += enc_key
    data += enc_data

    data = add_header(data, data_header, False)
    return data, data_header.id


# 获取同花顺连接数据包
def get_hexin_connect_data(passport_dat):
    if passport_dat != b'':
        data_header = MiniDataHead()
        data_header.headLength = 28
        data_header.id = get_pack_id()
        data_header.type = 0x70000
        data_header.dataLength = len(passport_dat)
        data = add_header(passport_dat, data_header, False)
        return data, data_header.id

    str_info = 'ScreenWidth=720'
    str_info += '\r\nScreenHeight=1280'
    str_info += '\r\nsmallestWidth=0dp'
    str_info += '\r\ndensity=1.0'
    str_info += '\r\nrealdata=true'
    str_info += '\r\ntime2012=1'
    str_info += '\r\nAppletVersion=' + constants.APPLET_VERSION
    str_info += '\r\nsvnver=' + constants.SVN_VER
    str_info += '\r\nTestVersion=' + constants.TEST_VERSION
    str_info += '\r\nBranchName=' + constants.BRANCH_NAME
    str_info += '\r\nFunClientSupport=0111111111100011111111'
    str_info += '\r\napp=android'
    str_info += '\r\nfor=ths_am_gphone_login'
    str_info += '\r\nprogid=500'
    str_info += '\r\nnet=1'
    str_info += '\r\nqsid=800'
    str_info += '\r\nsourceid=' + constants.SOURCE_ID
    str_info += '\r\nspcode=' + constants.SP_CODE
    str_info += '\r\nchannelid=' + constants.SOURCE_ID
    str_info += '\r\ntype=' + constants.TYPE
    str_info += '\r\nudid=' + constants.UDID
    str_info += '\r\nimei=' + constants.IMEI
    str_info += '\r\nsim=' + constants.UDID
    str_info += '\r\nimsi=' + constants.IMSI
    str_info += '\r\nmacA=' + constants.MAC
    str_info += '\r\nsdk=22'
    str_info += '\r\nsdkn=5.1.1'
    str_info += '\r\nCA=4'
    str_info += '\r\ndev=' + constants.DEV
    str_info += '\r\n'

    data = b''
    for i in range(len(str_info)):
        data += int.to_bytes(ord(str_info[i]), 2, byteorder='little', signed=False)

    data = int.to_bytes(len(str_info), 2, byteorder='little', signed=False) + data

    # data长度不够8的倍数则用00补齐
    data += b"\x00\x00\x00\x00\x00\x00\x00"
    data = data[0:int(len(data) / 8) * 8]

    data_header = MiniDataHead()
    data_header.headLength = 28
    data_header.id = get_pack_id()
    data_header.type = 0x70000
    data_header.dataLength = len(data)
    data = add_header(data, data_header, False)

    return data, data_header.id


# 获取同花顺登录手机验证码数据包
def get_hexin_login_sms_data(account):
    reqpage = random.randint(10000, 99999).__str__()
    enc_account = base64.b64encode(rsa_utils.rsa_encrypt(account.encode('utf-8')))
    enc_account = parse.quote(enc_account)
    url = 'verify?reqtype=wlh_thsreg_modify&mobile_login=1&qsid=800&regflag&udid=' + constants.UDID + '&encoding=GBK&mobile=' + enc_account + '&rsa_version=default_4&foreign=1&foreign_country=86'
    str_info = '[frame]'
    str_info += '\r\nid=4222'
    str_info += '\r\npageList=' + reqpage
    str_info += '\r\nreqPage=' + reqpage
    str_info += '\r\nreqPageCount=1'
    str_info += '\r\n[' + reqpage + ']'
    str_info += '\r\nid=1101'
    str_info += '\r\nhost=auth'
    str_info += '\r\nurl=' + url
    str_info += '\r\n'

    data_header = MiniDataHead()
    data_header.headLength = 28
    data_header.id = get_pack_id()
    data_header.frameId = 0x107E
    data_header.textLength = len(str_info)
    data = add_header(str_info.encode(), data_header, False)
    return data, data_header.id


# 获取同花顺登录数据包, 当isSMS为True时, 意味着为验证码登录, password填写验证码就行
def get_hexin_login_data(account, password, isSMS):
    reqpage = random.randint(10000, 99999).__str__()

    enc_account = base64.b64encode(rsa_utils.rsa_encrypt(account.encode('utf-8')))
    enc_account = str(enc_account, 'utf-8')
    enc_password = base64.b64encode(rsa_utils.rsa_encrypt(password.encode('utf-8')))
    enc_password = str(enc_password, 'utf-8')

    str_info = '[frame]'
    str_info += '\r\nid=2054'
    str_info += '\r\npageList=' + reqpage
    str_info += '\r\nreqPage=' + reqpage
    str_info += '\r\nreqPageCount=1'
    str_info += '\r\n[' + reqpage + ']'
    str_info += '\r\nid=1001'
    str_info += '\r\ncrypt=2'
    str_info += '\r\nctrlcount=2'
    str_info += '\r\nctrlid_0=34338'
    str_info += '\r\nctrlvalue_0=' + enc_account
    str_info += '\r\nctrlid_1=34339'
    str_info += '\r\nctrlvalue_1=' + enc_password
    str_info += '\r\nreqctrl=4304'
    str_info += '\r\nloginmode=1'
    if not isSMS:
        str_info += '\r\nloginType=3\r\n'
    else:
        str_info += '\r\nforeign=1'
        str_info += '\r\nforeign_country=86'
        str_info += '\r\nloginType=7\r\n'

    data_header = MiniDataHead()
    data_header.headLength = 28
    data_header.id = get_pack_id()
    data_header.frameId = 0x806
    data_header.textLength = len(str_info)
    data = add_header(str_info.encode(), data_header, False)

    return data, data_header.id


# 获取可转债/股票行情数据包
def get_prepurchase_data(code, price, quantity):
    reqpage = random.randint(10000, 99999).__str__()
    str_info = '[frame]'
    str_info += '\r\nid=2682'
    str_info += '\r\npageList=' + reqpage
    str_info += '\r\nreqPage=' + reqpage
    str_info += '\r\nreqPageCount=1'
    str_info += '\r\nqsid=' + globals()['qsid']
    str_info += '\r\nwtaccount=' + globals()['wtaccount']
    str_info += '\r\nwttype=' + globals()['dtkltype']
    str_info += '\r\n[' + reqpage + ']'
    str_info += '\r\nid=1804'
    str_info += '\nctrlid_0=2102'
    str_info += '\nctrlvalue_0=' + code
    str_info += '\nctrlid_1=2127'
    str_info += '\nctrlvalue_1=' + price
    str_info += '\nreqctrl=4507'
    str_info += '\nctrlid_2=36615'
    str_info += '\nctrlvalue_2=' + quantity
    str_info += '\nctrlcount=3'
    str_info += '\r\nHDInfo=' + constants.HD_INFO
    data_header = MiniDataHead()
    data_header.headLength = 28
    data_header.id = get_pack_id()
    data_header.frameId = 0xA7A
    data_header.textLength = len(str_info)
    data = add_header(str_info.encode(), data_header, True)
    return data, data_header.id


# 获取可转债/股票行情数据包
def get_price_data_4491(code):
    reqpage = random.randint(10000, 99999).__str__()
    str_info = '[frame]'
    str_info += '\r\nid=2682'
    str_info += '\r\npageList=' + reqpage
    str_info += '\r\nreqPage=' + reqpage
    str_info += '\r\nreqPageCount=1'
    str_info += '\r\nqsid=' + globals()['qsid']
    str_info += '\r\nwtaccount=' + globals()['wtaccount']
    str_info += '\r\nwttype=' + globals()['dtkltype']
    str_info += '\r\n[' + reqpage + ']'
    str_info += '\r\nid=1804'
    str_info += "\r\nreqtype=262144"
    str_info += '\nctrlid_0=2102'
    str_info += '\nctrlvalue_0=' + code
    str_info += '\nctrlid_1=2218'
    str_info += '\nctrlvalue_1=1'
    str_info += '\nctrlid_2=2219'
    str_info += '\nctrlvalue_2=1'
    str_info += '\nreqctrl=4491'
    str_info += '\nctrlcount=3'
    str_info += '\r\nHDInfo=' + constants.HD_INFO
    data_header = MiniDataHead()
    data_header.headLength = 28
    data_header.id = get_pack_id()
    data_header.frameId = 0xA7A
    data_header.textLength = len(str_info)
    data = add_header(str_info.encode(), data_header, True)
    return data, data_header.id


# 获取可转债/股票行情数据包
def get_price_data_4492(code, price):
    reqpage = random.randint(10000, 99999).__str__()
    str_info = '[frame]'
    str_info += '\r\nid=2682'
    str_info += '\r\npageList=' + reqpage
    str_info += '\r\nreqPage=' + reqpage
    str_info += '\r\nreqPageCount=1'
    str_info += '\r\nqsid=' + globals()['qsid']
    str_info += '\r\nwtaccount=' + globals()['wtaccount']
    str_info += '\r\nwttype=' + globals()['dtkltype']
    str_info += '\r\n[' + reqpage + ']'
    str_info += '\r\nid=1804'
    str_info += "\r\nreqtype=262144"
    str_info += '\nreqctrl=4492'
    str_info += '\nctrlid_0=2127'
    str_info += '\nctrlvalue_0=' + price
    str_info += '\nctrlid_1=2102'
    str_info += '\nctrlvalue_1=' + code
    str_info += '\nctrlcount=2'
    str_info += '\r\nHDInfo=' + constants.HD_INFO
    data_header = MiniDataHead()
    data_header.headLength = 28
    data_header.id = get_pack_id()
    data_header.frameId = 0xA7A
    data_header.textLength = len(str_info)
    data = add_header(str_info.encode(), data_header, True)
    return data, data_header.id


# 获取申购可转债数据包
def get_purchase_data(code, price, quantity):
    reqpage = random.randint(10000, 99999).__str__()
    str_info = '[frame]'
    str_info += '\r\nid=2682'
    str_info += '\r\npageList=' + reqpage
    str_info += '\r\nreqPage=' + reqpage
    str_info += '\r\nreqPageCount=1'
    str_info += '\r\nqsid=' + globals()['qsid']
    str_info += '\r\nwtaccount=' + globals()['wtaccount']
    str_info += '\r\nwttype=' + globals()['dtkltype']
    str_info += '\r\n[' + reqpage + ']'
    str_info += '\r\nid=1820'
    str_info += '\r\nreqctrl=2001'
    str_info += '\nctrlid_0=36641'
    str_info += '\nctrlvalue_0=1'
    str_info += '\nctrlid_1=36615'
    str_info += '\nctrlvalue_1=' + quantity
    str_info += '\nctrlid_2=2102'
    str_info += '\nctrlvalue_2=' + code
    str_info += '\nctrlid_3=2127'
    str_info += '\nctrlvalue_3=' + price
    str_info += '\nctrlcount=4'
    str_info += '\r\nHDInfo=' + constants.HD_INFO
    data_header = MiniDataHead()
    data_header.headLength = 28
    data_header.id = get_pack_id()
    data_header.frameId = 0xA7A
    data_header.textLength = len(str_info)
    data = add_header(str_info.encode(), data_header, True)
    return data, data_header.id


# 获取新债数据，返回数据为申购代码列表
def get_cate_info():
    session = requests.session()
    res = session.get(constants.CATE_URL, verify=False, allow_redirects=False)
    task = []
    json_infos = json.loads(res.text)
    for info in json_infos:
        if info['sgDate'] == info['today']:
            task.append(info['sgCode'])
    return task


# 调用指定的获取数据包函数, 完成相应的数据包的发送和接收
def sendAndRecv(data_func, *args):
    data, id = data_func(*args)
    if constants.log == 1:
        print(data_func.__name__ + ':' + data.hex())
    tcp_client_socket.send(data)
    ret_data = recv_factory(id=id)
    return ret_data


# 创建一个tcp连接
tcp_client_socket = socket(AF_INET, SOCK_STREAM)
try:
    if constants.debug != 1:
        tcp_client_socket.connect((constants.CONNECT_HOST, constants.CONNECT_PORT))
    print("connect success!")
except Exception as err:
    print(err)
    sys.exit(0)

# 全局数据包ID,该ID不可重复
pack_id = 0

# 后续生成数据需要用到
qs_login_header = b''

# 会话密钥,随机生成，可固定
server_key = b''
for _ in range(16):
    server_key += int.to_bytes(random.randint(0, 255), 1, byteorder='little', signed=False)

# 券商账户
wtaccount = ''
# 券商密码
wtpassword = ''
# 券商参数
qsid = ''
wtid = ''
dtkltype = ''

# 测试的时候, 部分参数需要固定
if constants.debug == 1:
    pack_id = 43
    qs_login_header = b''
    server_key = bytes.fromhex(''.replace(" ", ""))

if constants.log == 1:
    print("server_key:", server_key.hex())

# 获取可转债信息
cate_info = get_cate_info()

if constants.debug != 1 and len(cate_info) > 0:

    passport_dat = b''
    # 尝试读取passport.dat文件
    if os.path.exists('passport.dat'):
        with open("passport.dat", mode='rb') as f:
            passport_dat = f.read()

    # 获取连接数据
    ret_data = sendAndRecv(get_hexin_connect_data, passport_dat)

    # 第一次需要手机号登录一下, 后续不再需要
    if ret_data == '需要手机号登录':
        while True:
            account = input('输入同花顺手机号:')
            ret_data = sendAndRecv(get_hexin_login_sms_data, account)
            if ret_data.find('ret code="0"') == -1:
                print('短信验证码发送失败')
                print(ret_data)
            break

        while True:
            data = input('输入验证码:')
            ret_data = sendAndRecv(get_hexin_login_data, account, data, True)
            if ret_data != '登录成功':
                print('验证码校验失败')
                print(ret_data)
            break

    elif ret_data != '登录成功':
        print('未知错误')
        print(ret_data)
        sys.exit(0)

    # 同花顺登录成功后尝试登录证券
    ret_data = sendAndRecv(get_qs_login_data, wtaccount, wtpassword, '', qsid, wtid, dtkltype)
    if ret_data != '证券登录成功':
        print('证券登录失败')
        print(ret_data)
        sys.exit(0)

    # 证券登录成功后尝试申购可转债
    for code in cate_info:
        price = '100.000'
        quantity = '10000'

        # 获取可转债信息
        ret_data = sendAndRecv(get_price_data_4491, code)
        if ret_data.find(code) == -1:
            print('申购失败-->' + ret_data)
            continue

        # 类似于生成订单, 需要确认提交
        ret_data = sendAndRecv(get_prepurchase_data, code, price, quantity)
        if ret_data.find('您是否确认以上委托?') == -1:
            print('申购失败-->' + ret_data)
            continue
        print(ret_data)

        # 提交申购请求
        ret_data = sendAndRecv(get_purchase_data, code, price, quantity)
        if ret_data.find('委托已提交') == -1:
            print('申购失败-->' + ret_data)
            continue
        print(ret_data)
else:
    # 这部分主要放测试组包/解包时候的代码
    pass
