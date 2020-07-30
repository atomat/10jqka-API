from OutputStream import OutputStream


class stuffInteractData:
    title = ''
    content = ''
    confirm = ''
    cancel = ''
    id = 0
    type = 0

    def __init__(self, InputStream):
        decode_Data = OutputStream(InputStream)

        self.title = decode_Data.readUTF()
        self.content = decode_Data.readUTF()
        if self.content == '':
            self.content == '操作频繁,请稍后再试'

        length = decode_Data.readUnsignedShort()
        if length > 0:
            self.confirm = decode_Data.readUnicode2UTF8(length)

        length = decode_Data.readUnsignedShort()
        if length > 0:
            self.cancel = decode_Data.readUnicode2UTF8(length)

        if decode_Data.available() >= 6:
            decode_Data.skipBytes(2)
            self.type = decode_Data.readInt()

        if decode_Data.available() >= 6:
            decode_Data.skipBytes(2)
            self.id = decode_Data.readInt()