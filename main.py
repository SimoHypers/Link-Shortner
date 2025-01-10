import requests
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class LinkShortner(QWidget):
    def __init__(self):
        super().__init__()
        self.original_link_label = QLabel("Enter a link: ", self)
        self.original_link_input = QLineEdit(self)
        self.link_name_label = QLabel("Enter a link name: (Optional)", self)
        self.link_name_input = QLineEdit(self)
        self.get_link_button = QPushButton("Get Link", self)
        self.short_link_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Link Shortner")
        self.setWindowIcon(QIcon("link.png"))
        vbox = QVBoxLayout()

        vbox.addWidget(self.original_link_label)
        vbox.addWidget(self.original_link_input)
        vbox.addWidget(self.link_name_label)
        vbox.addWidget(self.link_name_input)
        vbox.addWidget(self.get_link_button)
        vbox.addWidget(self.short_link_label)

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

            """
        )

        self.get_link_button.clicked.connect(self.shorten_link)


    def shorten_link(self):
        original_link = self.original_link_input.text()
        link_name = self.link_name_input.text()

        # Check for empty input
        if not original_link.strip():
            self.short_link_label.setText("Enter a valid link.")
            return

        API_KEY = '87b15d971ffa5ced2664ddba7caf46e9d8b57'
        BASE_URL = 'https://cutt.ly/api/api.php'

        payload = {
            'key': API_KEY,
            'short': original_link,
            'name': link_name
        }

        try:
            response = requests.get(BASE_URL, params=payload)

            data = response.json()
            status = data['url']['status']

            if status == 7:  # Success
                title = data['url'].get('title', 'No title')
                short_link = data['url']['shortLink']
                self.short_link_label.setText(short_link)
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
                    7: "Unknown error occurred.",
                }.get(status, "Unknown error occurred.")
                self.short_link_label.setText(f"Error: {error_message}")
                print(f"Error Status: {status}, {error_message}")
        except Exception as e:
            self.short_link_label.setText("An error occurred.")
            print(f"Exception: {e}")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    linkshortner_app = LinkShortner()
    linkshortner_app.show()
    sys.exit(app.exec_())