import requests
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QClipboard
from dotenv import load_dotenv
import os

load_dotenv()

class LinkShortner(QWidget):
    def __init__(self):
        super().__init__()
        self.original_link_label = QLabel("Enter a link: ", self)
        self.original_link_input = QLineEdit(self)
        self.link_name_label = QLabel("Enter a link name: (Optional)", self)
        self.link_name_input = QLineEdit(self)
        self.get_link_button = QPushButton("Get Link", self)
        self.short_link_label = QLabel(self)
        self.copy_url_button = QPushButton("Copy URL to Clipboard", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Link Shortener")
        self.setWindowIcon(QIcon("link.png"))
        vbox = QVBoxLayout()

        vbox.addWidget(self.original_link_label)
        vbox.addWidget(self.original_link_input)
        vbox.addWidget(self.link_name_label)
        vbox.addWidget(self.link_name_input)
        vbox.addWidget(self.get_link_button)
        vbox.addWidget(self.short_link_label)
        vbox.addWidget(self.copy_url_button)

        self.setLayout(vbox)

        self.original_link_label.setAlignment(Qt.AlignCenter)
        self.original_link_input.setAlignment(Qt.AlignCenter)
        self.link_name_label.setAlignment(Qt.AlignCenter)
        self.link_name_input.setAlignment(Qt.AlignCenter)
        self.short_link_label.setAlignment(Qt.AlignCenter)

        self.original_link_label.setObjectName("original_link_label")
        self.original_link_input.setObjectName("original_link_input")
        self.link_name_label.setObjectName("link_name_label")
        self.link_name_input.setObjectName("link_name_input")
        self.get_link_button.setObjectName("get_link_button")
        self.short_link_label.setObjectName("short_link_label")
        self.copy_url_button.setObjectName("copy_url_button")

        self.setStyleSheet("""
            QLabel, QPushButton {
                    font-family: calibri;
                }
            QLabel#original_link_label {
                    font-size: 20px;
                    font-style: italic;
                }
            QLineEdit#original_link_input {
                    font-size: 20px;
                    padding: 5px;
                }
            QLabel#link_name_label {
                    font-size: 20px;
                    font-style: italic;
                }
            QLineEdit#link_name_input {
                    font-size: 20px;
                    padding: 5px;
                }
            QPushButton#get_link_button {
                    font-size: 15px;
                    font-weight: bold;
                    padding: 5px;
                }
            QLabel#short_link_label {
                    font-size: 50px;
                }
            QPushButton#copy_url_button {
                    font-size: 15px;
                    font-weight: bold;
                    padding: 5px;
                }

            """
        )

        self.get_link_button.clicked.connect(self.shorten_link)
        self.copy_url_button.clicked.connect(self.copyToClipBoard)


    def shorten_link(self):
        original_link = self.original_link_input.text().strip()
        link_name = self.link_name_input.text().strip()

        if not original_link:
            self.short_link_label.setText("Enter a valid link.")
            return

        load_dotenv()
        API_KEY = os.getenv('API_KEY')

        if not API_KEY:
            self.short_link_label.setText("API Key not found. Check your configuration.")
            return

        BASE_URL = 'https://cutt.ly/api/api.php'

        payload = {
            'key': API_KEY,
            'short': original_link,
            'name': link_name
        }

        try:
            response = requests.get(BASE_URL, params=payload)
            response.raise_for_status()
            data = response.json()

            status = data['url']['status']

            if status == 7:  # Success
                title = data['url'].get('title', 'No title')
                short_link = data['url']['shortLink']
                self.short_link_label.setText(f"{short_link}")
                print(f"Title: {title}")
                print(f"Short Link: {short_link}")
            else:
                error_message = {
                    1: "The link you entered is invalid.",
                    2: "The entered link is already shortened.",
                    3: "The domain used is blacklisted.",
                    4: "The URL contains invalid characters.",
                    5: "The provided key is invalid.",
                    6: "The link name is already taken.",
                }.get(status, "Unknown error occurred.")
                self.short_link_label.setText(f"Error: {error_message}")
                print(f"Error Status: {status}, {error_message}")
        except Exception as e:
            self.short_link_label.setText("An error occurred. Try again.")
            print(f"Exception: {e}")
    
    def copyToClipBoard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.short_link_label.text())
        self.short_link_label.setText("Link copied to clipboard!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    linkshortner_app = LinkShortner()
    linkshortner_app.show()
    sys.exit(app.exec_())