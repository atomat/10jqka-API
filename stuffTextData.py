from OutputStream import OutputStream


class stuffTextData:
    title = ''
    content = ''
    type = 0
    id = 0
    reCode = 0

    def __init__(self, data_type, InputStream):
        decode_Data = OutputStream(InputStream)

        self.title = decode_Data.readUTF()
        self.content = decode_Data.readUTF()
        if self.content == '':
            self.content == '操作频繁,请稍后再试'

        self.type = data_type & 0xF0
        if self.type == 0:
            self.type == 1
        elif self.type == 16:
            self.type == 2
        elif self.type == 32:
            self.type == 3
        elif self.type == 15 or self.type == 48:
            self.type == 4
        elif self.type == 64:
            self.type == 5

        if decode_Data.available() >= 6:
            decode_Data.skipBytes(2)
            self.id = decode_Data.readInt()

        if decode_Data.available() >= 6:
            decode_Data.skipBytes(2)
            self.reCode = decode_Data.readInt()

    def toList(self):
        data = {'title': self.title, 'content': self.content, 'type': self.type, 'id': self.id, 'reCode': self.reCode}
