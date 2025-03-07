import base64

class Еncoder:
    @staticmethod
    def encode(data: str) -> str:
        bytes_data = data.encode('utf-8')
        encoded_data = base64.b64encode(bytes_data)
        return encoded_data.decode('utf-8')

    @staticmethod
    def decode(encoded_data: str) -> str:
        bytes_encoded = encoded_data.encode('utf-8')
        decoded_data = base64.b64decode(bytes_encoded)
        return decoded_data.decode('utf-8')

encoded_data =Еncoder.encode('1445048965:AAEon3ejkn9RexdJoqs_VCEUsTTQtY-vYPQ')
encoded='NzY0Nzc3MjI2MjpBQUVxbzd1T3BhNUJRU09aSC1WbnByajBHNlBJZ3J2bFBucw=='
decoded_key = Еncoder.decode(encoded_data)
