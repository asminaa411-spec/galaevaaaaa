import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, 
    QLineEdit, QComboBox, QPushButton, QTextEdit, QMessageBox
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.make_ui()
        
    def make_ui(self):
        self.setWindowTitle("Конвертер валют")
        self.resize(380, 400)
        
        lay = QVBoxLayout()
        
        lay.addWidget(QLabel("<b>Перевод валют</b>"))
        
        lay.addWidget(QLabel("Сумма:"))
        self.sum_input = QLineEdit()
        lay.addWidget(self.sum_input)
        
        lay.addWidget(QLabel("Из:"))
        self.combo1 = QComboBox()
        self.combo1.addItems(["USD", "EUR", "RUB", "GBP", "JPY", "CNY"])
        lay.addWidget(self.combo1)
        
        lay.addWidget(QLabel("В:"))
        self.combo2 = QComboBox()
        self.combo2.addItems(["USD", "EUR", "RUB", "GBP", "JPY", "CNY"])
        lay.addWidget(self.combo2)
        
        self.btn = QPushButton("Конвертировать")
        self.btn.clicked.connect(self.do_convert)
        lay.addWidget(self.btn)
        
        lay.addWidget(QLabel("Результат:"))
        self.res_box = QTextEdit()
        self.res_box.setReadOnly(True)
        lay.addWidget(self.res_box)
        
        self.setLayout(lay)
        
    def do_convert(self):
        try:
            val = float(self.sum_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите число!")
            return
            
        frm = self.combo1.currentText()
        to = self.combo2.currentText()
        
        payload = {
            "amount": val,
            "from_curr": frm,
            "to_curr": to
        }
        
        try:
            r = requests.post("http://127.0.0.1:8000/convert", json=payload, timeout=5)
        except requests.exceptions.ConnectionError:
            self.res_box.setText("Сервер не запущен!")
            return
        except Exception:
            self.res_box.setText("Ошибка сети")
            return
            
        print(r.status_code)
        
        if r.status_code == 200:
            data = r.json()
            self.res_box.setText(data["message"])
        else:
            err = r.json().get("error", "что-то пошло не так")
            self.res_box.setText("Ошибка: " + err)
            QMessageBox.warning(self, "Внимание", err)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())