from socket import *
import json
import datetime
import logging
import warnings
import threading
import time
import  sys


class logabc:
    def __init__(self):
        tcpCliSock = self.connects()
        logger = self.log_put()
        # while True:
        print("------------------------------------")
        print("|                                  |")
        print("|                start             |")
        print("|                                  |")
        print("---------------- -------------------")
        # 接受信息做一个线程
        print("请输入命令…………")
        time.sleep(1)
        recv_thread = threading.Thread(target=self.recv_file, args=(tcpCliSock, logger, ))
        recv_thread.daemon = True
        recv_thread.start()
        time.sleep(1)
        # 发送信息
        self.sends_file(tcpCliSock, logger, )
        tcpCliSock.close
    def connects(self):
        HOST = ('192.168.110.111')
        PORT = 8091
        ADDR = (HOST, PORT)
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        if len(sys.argv) > 3:
            print ("Correct usage: script, IP address, port number")
        if len(sys.argv) > 1:
            HOST = str(sys.argv[1])
        else:
            HOST = ('192.168.110.111')

        if len(sys.argv) > 2:
            HOST = str(sys.argv[2])
        else:
            PORT = 8091

        # PORT = int(sys.argv[2])
        ADDR = (HOST, PORT)
        tcpCliSock.connect(ADDR)

        print("connect ：",HOST,PORT)
        return tcpCliSock


    def time_now(self):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time

    def log_put(self):
        # log信息输出

        warnings.filterwarnings("ignore", category=UserWarning)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)
        logger = logging.getLogger(__name__)

        file_handler = logging.FileHandler('application.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S'))
        logger.addHandler(file_handler)
        return logger

    def recv_file(self,tcpCliSock,logger,):
        # 接受数据
        new_msg = ""
        while True:
            #lock_recv.acquire()
            #lock_recv.release()
            #print("first = ",recv_data[-2:],b'\r\n' in recv_data)
            #flag = new_data[-1].find("\r")
            #print("flag= ",flag,'\r\n' in recv_data)
            #expect = b'\r\n'

            #接受信息 是以 字符输出
            recv_data_init = tcpCliSock.recv(10240)

            #对 字节数据进行转换，变成字符类型
            new_data = recv_data_init.decode(encoding="utf-8",errors="ignore")

            # 判断 信息是否接受完整
            if '\r\n' in  new_data:
                new_msg += new_data
            else:
                new_msg += new_data
                continue

            time.sleep(1)

            #数据进行处理
            #msg_total = str(new_msg)
            #msg_total = str.replace(msg_total,"},", "}").replace('\n', '')
            #msg_total = msg_total.strip('\n')
            #msg_total = msg_total.strip('')
            #msg_total = msg_total.split("}")

            #数据进行处理----->testq

            # <class 'str'>
            msg_total = new_msg[:-3]
            msg_total = msg_total.split("}")


            time.sleep(1)

            #输出数据
            for i in msg_total:
                i = i.replace(",{", "{").strip("\n").strip("")
                logger.info("{}".format(i))

            new_msg = ""

            #if expect in recv_data_init :
                #break

    def sends_file(self,tcpCliSock,logger,):
        # 发送数据
        while True:

            time.sleep(1)
            send_data = input() or {"version": 1, "uuid": 1234, "type": "all", "method": "c.query"}
            if send_data == 'q' or send_data == "q":
                break
            if isinstance(send_data,dict):
                send_data = json.dumps(send_data)
            try:
                send_data += "\r\n"
            except Exception as e:
                raise TypeError("这个不是一个字符串")

            #获取当前时间
            aa = self.time_now()
            print(f"{aa}用户输入agine:  \n",send_data)


            tcpCliSock.sendall(send_data.encode())

if __name__ == "__main__":
    ui = logabc()