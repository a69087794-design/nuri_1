import sys
import os
import asyncio
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor
from dotenv import load_dotenv
load_dotenv()


class NuriLoader(QThread):
    """NURICore ni alohida threadda yuklaydigan sinf"""
    finished   = pyqtSignal(object)   # nuri_core
    error      = pyqtSignal(str)

    def run(self):
        try:
            from main import NURICore
            core = NURICore()
            self.finished.emit(core)
        except Exception as e:
            self.error.emit(str(e))


class WorkerThread(QThread):
    result_ready = pyqtSignal(str)

    def __init__(self, nuri_core, command):
        super().__init__()
        self.nuri_core = nuri_core
        self.command   = command

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                self.nuri_core.process_command(self.command)
            )
            self.result_ready.emit(result or "")
        except Exception as e:
            self.result_ready.emit(f"Xatolik: {e}")
        finally:
            loop.close()


class NuriGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NURI — Neyronli Universal Robot Intellekti")
        self.setMinimumSize(900, 650)
        self.nuri_core     = None
        self.worker        = None
        self.authenticated = False
        self.loader        = None

        self.setup_ui()
        self.setup_style()
        self.start_loading()

    def start_loading(self):
        self.loader = NuriLoader()
        self.loader.finished.connect(self._on_loaded)
        self.loader.error.connect(self._on_load_error)
        self.loader.start()

    def _on_loaded(self, core):
        self.nuri_core = core
        self.status_label.setText("● Tayyor — Parol kiriting")
        self.role_badge.setText("Kirish kerak")
        self.send_btn.setEnabled(True)
        self.input_field.setEnabled(True)
        self.add_message("NURI", "Tizim yuklandi! Parolni kiriting.", "nuri")

    def _on_load_error(self, error):
        self.status_label.setText("● Xato!")
        self.role_badge.setText("Xato")
        self.add_message("Tizim", f"Yuklashda xato: {error}", "system")

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(60)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(16, 0, 16, 0)

        logo = QLabel("N")
        logo.setObjectName("logo")
        logo.setFixedSize(36, 36)
        logo.setAlignment(Qt.AlignCenter)
        h_layout.addWidget(logo)

        info = QVBoxLayout()
        info.setSpacing(0)
        self.title_label = QLabel("NURI")
        self.title_label.setObjectName("titleLabel")
        self.status_label = QLabel("Yuklanmoqda...")
        self.status_label.setObjectName("statusLabel")
        info.addWidget(self.title_label)
        info.addWidget(self.status_label)
        h_layout.addLayout(info)
        h_layout.addStretch()

        self.role_badge = QLabel("Yuklanmoqda...")
        self.role_badge.setObjectName("roleBadge")
        h_layout.addWidget(self.role_badge)
        main_layout.addWidget(header)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("separator")
        main_layout.addWidget(sep)

        # Chat
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setObjectName("chatArea")
        main_layout.addWidget(self.chat_area)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setObjectName("separator")
        main_layout.addWidget(sep2)

        # Footer
        footer = QFrame()
        footer.setObjectName("footer")
        footer.setFixedHeight(64)
        f_layout = QHBoxLayout(footer)
        f_layout.setContentsMargins(16, 12, 16, 12)
        f_layout.setSpacing(8)

        self.input_field = QLineEdit()
        self.input_field.setObjectName("inputField")
        self.input_field.setPlaceholderText("Yuklanmoqda, kuting...")
        self.input_field.setEnabled(False)
        self.input_field.returnPressed.connect(self.send_message)
        f_layout.addWidget(self.input_field)

        self.mic_btn = QPushButton("🎤")
        self.mic_btn.setObjectName("micBtn")
        self.mic_btn.setFixedWidth(44)
        self.mic_btn.clicked.connect(self.voice_input)
        f_layout.addWidget(self.mic_btn)

        self.send_btn = QPushButton("Yuborish")
        self.send_btn.setObjectName("sendBtn")
        self.send_btn.setFixedWidth(100)
        self.send_btn.setEnabled(False)
        self.send_btn.clicked.connect(self.send_message)
        f_layout.addWidget(self.send_btn)

        main_layout.addWidget(footer)

        self.add_message("NURI", "Assalomu alaykum! Tizim yuklanmoqda...", "nuri")

    def setup_style(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a2e; }
            QWidget { background-color: #1a1a2e; color: #e0e0e0;
                      font-family: 'Segoe UI', Arial, sans-serif; }
            QFrame#header { background-color: #16213e; }
            QFrame#footer { background-color: #16213e; }
            QFrame#separator { background-color: #0f3460; max-height: 1px; }
            QLabel#titleLabel { color: #e0e0e0; font-size: 15px; font-weight: bold; }
            QLabel#statusLabel { color: #81c784; font-size: 11px; }
            QLabel#logo { background-color: #533483; color: white;
                          font-size: 16px; font-weight: bold; border-radius: 18px; }
            QLabel#roleBadge { background-color: #0f3460; color: #b39ddb;
                               font-size: 11px; padding: 4px 12px;
                               border-radius: 6px; border: 1px solid #533483; }
            QTextEdit#chatArea { background-color: #1a1a2e; border: none;
                                 padding: 16px; font-size: 13px; color: #e0e0e0; }
            QLineEdit#inputField { background-color: #1a1a2e;
                                   border: 1px solid #0f3460;
                                   border-radius: 8px; padding: 8px 14px;
                                   color: #e0e0e0; font-size: 13px; }
            QLineEdit#inputField:focus { border: 1px solid #533483; }
            QLineEdit#inputField:disabled { color: #555555; }
            QPushButton#sendBtn { background-color: #533483; color: white;
                                  border: none; border-radius: 8px;
                                  font-size: 13px; font-weight: bold; }
            QPushButton#sendBtn:hover { background-color: #6a45a0; }
            QPushButton#sendBtn:pressed { background-color: #3d2566; }
            QPushButton#sendBtn:disabled { background-color: #2a1a4a; color: #666; }
            QPushButton#micBtn { background-color: #0f3460;
                                 border: 1px solid #533483;
                                 border-radius: 8px; font-size: 15px; }
            QPushButton#micBtn:hover { background-color: #1a4a80; }
            QScrollBar:vertical { background: #16213e; width: 6px; border-radius: 3px; }
            QScrollBar::handle:vertical { background: #533483; border-radius: 3px; }
        """)

    def add_message(self, sender: str, message: str, msg_type: str = "nuri"):
        if msg_type == "user":
            color, align, bg = "#4fc3f7", "right", "#0f3460"
        elif msg_type == "nuri":
            color, align, bg = "#81c784", "left", "#16213e"
        else:
            color, align, bg = "#ffb74d", "left", "#1a1a2e"

        html = (
            f'<div style="text-align:{align}; margin:6px 0;">'
            f'<span style="color:{color}; font-size:11px; font-weight:bold;">{sender}</span><br>'
            f'<span style="display:inline-block; background:{bg}; '
            f'padding:8px 12px; border-radius:10px; font-size:13px; '
            f'max-width:75%; white-space:pre-wrap; word-wrap:break-word;">'
            f'{message.replace(chr(10), "<br>")}</span>'
            f'</div><br>'
        )
        self.chat_area.append(html)
        self.chat_area.moveCursor(QTextCursor.End)

    def send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return
        self.input_field.clear()

        if not self.authenticated:
            self._try_login(text)
            return

        if text.lower() in ("chiqish", "exit", "quit"):
            self.close()
            return

        self.add_message("Siz", text, "user")
        self.send_btn.setEnabled(False)
        self.input_field.setEnabled(False)
        self.status_label.setText("NURI o'ylayapti...")

        self.worker = WorkerThread(self.nuri_core, text)
        self.worker.result_ready.connect(self._on_response)
        self.worker.start()

    def _try_login(self, password: str):
        if self.nuri_core is None:
            self.add_message("Tizim", "NURI hali yuklanmoqda, kuting...", "system")
            return

        admin_pass = os.getenv("ADMIN_PASSWORD", "darling")

        if password == admin_pass:
            self.nuri_core.current_role = "admin"
            self.nuri_core.current_user = "admin"
            self.authenticated = True
            self.role_badge.setText("Admin")
            self.status_label.setText("● Admin rejimi")
            self.input_field.setPlaceholderText("Buyruq yoki savol yozing...")
            self.add_message("NURI", "Admin sifatida kirdingiz! Xush kelibsiz!", "nuri")
        else:
            from identity_engine import verify_user_password, get_username_by_password
            if verify_user_password(password):
                username = get_username_by_password(password) or "user"
                self.nuri_core.current_role = "user"
                self.nuri_core.current_user = username
                self.authenticated = True
                self.role_badge.setText(f"User: {username}")
                self.status_label.setText(f"● {username}")
                self.input_field.setPlaceholderText("Savol yoki buyruq yozing...")
                self.add_message("NURI", f"Xush kelibsiz, {username}!", "nuri")
            else:
                self.add_message("NURI", "Parol xato! Qayta urinib ko'ring.", "nuri")

    def _on_response(self, response: str):
        if response:
            self.add_message("NURI", response, "nuri")
        self.send_btn.setEnabled(True)
        self.input_field.setEnabled(True)
        self.input_field.setFocus()
        self.status_label.setText("● Faol")

    def voice_input(self):
        self.add_message("Tizim", "Ovozli kiritish ishlanmoqda...", "system")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NuriGUI()
    window.show()
    sys.exit(app.exec_())
