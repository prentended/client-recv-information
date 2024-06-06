import socket
import json
import sys
import datetime
import logging
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from QtTest import Ui_MainWindow  # Assuming this is a generated file from Qt Designer

# Configure logging to save logs to a file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("client_app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class ClientSocket:
    def __init__(self):
        self.tcpCliSock = None
        self.is_connected = False
        self.ip = ""
        self.port = 0

    def connect(self, ip, port):
        self.ip = ip
        self.port = port
        try:
            self.tcpCliSock = socket.socket()
            self.tcpCliSock.connect((self.ip, self.port))
            self.is_connected = True
            logging.info("Successfully connected to server.")
            return True
        except Exception as e:
            logging.error(f"Connection to server failed: {e}")
            return False

    def send_message(self, message):
        if not self.is_connected:
            logging.error("Server is not connected")
            return

        if not message.strip():
            message = {"version": 1, "uuid": 1234, "type": "all", "method": "c.query"}
        if isinstance(message, dict):
            message = json.dumps(message)
            logging.info("Converted dictionary to JSON string")
        elif isinstance(message, str):
            logging.info("Received a string message")
        else:
            logging.error("Unsupported message type")
            return

        message = message.strip() + "\r\n"
        logging.info(f"Sending message: {message}")
        try:
            self.tcpCliSock.send(message.encode())
            return message
        except Exception as e:
            logging.error(f"Failed to send message: {e}")

    def receive_messages(self, message_callback):
        try:
            new_msg = ""
            while True:
                response = self.tcpCliSock.recv(10240).decode(encoding="utf-8", errors="ignore")
                new_msg += response

                if '\r\n' in response:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message_callback(f"###{current_time}  Recv : ###")
                    count = new_msg.count("ECC57F")
                    message_callback(f"一共有 {count} 个设备")
                    new_msg = new_msg.replace("[{", "[\n{").replace(",{", "\n{")
                    message_callback(new_msg)
                    logging.info(f"Received message : {new_msg}")
                    new_msg = ""
        except Exception as e:
            logging.error(f"Error receiving messages: {e}")
            self.is_connected = False
            if self.tcpCliSock:
                self.tcpCliSock.close()


class ClientThread(QThread):
    message = pyqtSignal(str)

    def __init__(self):
        super(ClientThread, self).__init__()
        self.client_socket = ClientSocket()
        self.ip = ""
        self.port = 0

    def run(self):
        try:
            if self.client_socket.connect(self.ip, self.port):
                self.message.emit("服务端连接成功...")
                self.message.emit(f"ip:{self.ip}:{self.port}")
                self.client_socket.receive_messages(lambda msg: self.message.emit(msg))
            else:
                self.message.emit("连接服务端异常")
        except Exception as e:
            logging.error(f"An error occurred in client thread: {e}")

    @pyqtSlot(str, int)
    def connect_to_server(self, ip, port):
        self.ip = ip
        self.port = port
        if not self.isRunning():
            self.start()

    @pyqtSlot(str)
    def send_message(self, message):
        if self.client_socket.is_connected:
            sent_message = self.client_socket.send_message(message)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.message.emit(f"### {current_time}  Send :  ###\n {sent_message}")
        else:
            self.message.emit("server is not connected")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.worker = ClientThread()

        self.pushButton_2.clicked.connect(self.connect_server)
        self.worker.message.connect(self.handle_message)
        self.pushButton.clicked.connect(self.send_message)

    @pyqtSlot()
    def connect_server(self):
        ip = self.lineEdit.text().strip()
        port = int(self.lineEdit_2.text().strip())
        logging.info(f"Connecting to server {ip}:{port}")
        self.worker.connect_to_server(ip, port)

    @pyqtSlot(str)
    def handle_message(self, msg):
        self.textBrowser.append(msg)

    @pyqtSlot()
    def send_message(self):
        message_text = self.textEdit.toPlainText().strip()
        self.worker.send_message(message_text)
        QtWidgets.QApplication.processEvents()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())