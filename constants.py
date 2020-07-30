# 券商参数详见券商参数.txt

# 同花顺服务器地址和端口
CONNECT_HOST = 'mobi2.hexin.cn'
CONNECT_PORT = 9528

# 获取新债数据地址, 该接口可能不是很稳定
CATE_URL = 'http://data.hexin.cn/ipo/bond/cate/info/'

# 数据包的头部标志, 严格的说fd fd fd fd才是标志, 30 30 30 30是长度一部分, 不过这儿直接把它也算进来吧
DATA_MARK = b'\xfd\xfd\xfd\xfd\x30\x30\x30\x30'

# socket接收缓冲区大小
BUFFER_CACHE = 16 * 1024

# 加密_加密密钥rsa参数
RSA_E = 65537
RSA_N = 0xD78558CB2D5E06464BEFC2DDDD11AF1D7D7E2EDB0EE8CB6AE28901B21156970BDCD608C21273F394821199BD7C2D9ADA7BED2E3937235C5926B36094A2C67D97
RSA_KEY_HEADER = b'\x00\x02\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a' \
                 b'\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x00'

# 同花顺登录rsa密钥
RSA_KEY = '-----BEGIN PUBLIC KEY-----\n'\
          'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDLmaOkiR/+zt2U9FXFxIa5NtCj' \
          'ckfXUNKZ1mpxH198HvjBfq/S4VUggd/9H3iWZZPYGkmbgCsYsNdu8ddPIX4/2Y6O' \
          'BakGJFvt2BBVffuPZTEY5ZKToIweUd3PoswTJRpb4wGwgKDJOlh8txuu0Yrvnx4n' \
          '2mh3r+1rxWSdsS3QIQIDAQAB' \
          '\n-----END PUBLIC KEY-----'

# app信息, 不同版本的app以下信息不同, 正常情况下不需要改动, app更新时以下数据需要更新
# 应用版本号
APPLET_VERSION = 'G037.08.431.1.32'
# SVN版本号, 同花顺app大概采用SVN进行版本控制
SVN_VER = '38695f7fc663b7916de88c9b2ebcdda44e86a3de'
# 测试的版本号
TEST_VERSION = '57'
# 当前分支名称
BRANCH_NAME = 'K线分支'
# 渠道ID, 标志着app从哪儿下载
SOURCE_ID = '743'
# 表示此客户端是那个运营商的
SP_CODE = '9588000'
# #设备类型，发送给主站，默认为m, iptv, car, pda
DEV = 'm'
# 还有一些数据, 不是很重要, 直接固定在源码中, 没必要在这儿写出来了

# 多种设备信息
# 正式上线的时候TYPE/UDID/IMEI/IMSI/MAC地址需要根据自己的实际情况修改或者生成
# 如果需要生成, 可以调用utils模块中的函数进行生成
# 不可多个帐号共享设备信息
# TYPE代表机型
TYPE = ''
UDID = ''
IMEI = ''
IMSI = ''
MAC = ''
HD_INFO = 'MAC:' + MAC.replace(':', '-') + ',IMEI:' + IMEI + ',IMSI:' + IMSI

# debug为0,关闭调试功能,该模式下正常操作
# debug为1,开启调试功能,该模式下不进行网络连接
debug = 0

# log为1，开启详细日志功能，输出收发数据包内容
# log为0，关闭详细日志功能，不输出数据包详情，只输出关键的节点数据
log = 1




