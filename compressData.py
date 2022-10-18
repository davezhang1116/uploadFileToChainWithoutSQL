import gzip
import os

class compressData:
    def __init__(self, data):
        self.data=data

    def split_file(self, chunk_len, dir):
        try:
            data = gzip.compress(self.data)
            x = gzip.decompress(data_all)
        except:
            data = self.data
        
        os.mkdir(dir)
        file_size = len(data)
        chunks = [data[i:i+chunk_len] for i in range(0, file_size, chunk_len)]
        file_num = 0
        for i in chunks:
            file=open("./"+dir+"/{}.part".format(file_num), "wb")
            file.write(i)
            file.close()
            file_num=file_num+1
