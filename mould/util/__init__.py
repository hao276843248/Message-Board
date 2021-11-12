import os
import sys
import threading


class FileUtil:
    file_path = sys.path[0] + "/"
    file_name = "msg.db"

    def __init__(self):
        if not os.path.exists(self.file_path + self.file_name):
            open(self.file_path + self.file_name, "w+")

    def write(self, msg):
        if msg:
            with threading.Lock():
                with open(self.file_path + self.file_name, "a+") as f:
                    f.write(msg + "\n")

    def read_page(self, index):
        page_size = 10
        with threading.Lock():
            with open(self.file_path + self.file_name, "r") as f:
                data = f.readlines()
        data.reverse()
        return data[(index - 1) * page_size:index * page_size]

    def read(self):
        with threading.Lock():
            with open(self.file_path + self.file_name, "r") as f:
                data = f.readlines()
        data.reverse()
        return data

    def total(self):
        with threading.Lock():
            with open(self.file_path + self.file_name, "r") as f:
                return len(f.readlines())

    def delete(self, index):
        with threading.Lock():
            with open(self.file_path + self.file_name, "r") as f:
                msg = f.readlines()
            msg.reverse()
            msg.pop(index)
            msg.reverse()
            with open(self.file_path + self.file_name, "w") as f:
                f.write("".join(msg))


def message_filter(msg):
    msg = msg.replace("<", "&lt;")
    msg = msg.replace(">", "&gt;")
    msg = msg.replace("&", "&")
    msg = msg.replace("\"", "&quot;")
    msg = msg.replace("javascript", "java_script")
    msg = msg.replace("javaScript", "java_script")
    msg = msg.replace("script", "sp")
    return msg


FILE_UTIL = FileUtil()
