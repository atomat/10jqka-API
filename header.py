from OutputStream import OutputStream


class MiniDataHead:
    headLength = 0
    id = 0
    type = 0
    pageId = 0
    dataLength = 0
    frameId = 0
    textLength = 0
    sessionType = 0

    def __init__(self, *InputStream):
        if len(InputStream) <= 0:
            return
        decode_Data = OutputStream(InputStream[0])
        self.headLength = decode_Data.readUnsignedShort()
        self.id = decode_Data.readInt()
        self.type = decode_Data.readInt()
        self.frameId = decode_Data.readUnsignedShort()
        self.pageId = decode_Data.readInt()
        self.dataLength = decode_Data.readInt()
        self.textLength = decode_Data.readInt()
