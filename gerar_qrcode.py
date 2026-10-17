import sys
import io
import qrcode

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QLineEdit, QMessageBox
)
# Adicionado QIcon nas importações de arquivos gráficos
from PyQt6.QtGui import QPixmap, QFont, QImage, QIcon
from PyQt6.QtCore import Qt

class QRCodeApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator")
        self.setFixedSize(500, 650)
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: white; }
        """)
        
        # Configura o ícone da janela usando a imagem PNG local
        self.setWindowIcon(QIcon("d:/qrcode/qr-code.png"))
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(20)

        # TÍTULO
        self.title = QLabel("QR Code Generator")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.title.setStyleSheet("color: white; margin-top: 20px;")
        layout.addWidget(self.title)

        # INPUT
        self.input = QLineEdit()
        self.input.setPlaceholderText("Digite o texto ou código...")
        self.input.setMinimumHeight(55)
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #1E1E1E; border: 2px solid #333;
                border-radius: 15px; padding-left: 15px; color: white; font-size: 16px;
            }
            QLineEdit:focus { border: 2px solid #4A90E2; }
        """)
        layout.addWidget(self.input)

        # BOTÃO
        self.button = QPushButton("Gerar QR Code")
        self.button.setMinimumHeight(55)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2; border: none; border-radius: 15px;
                color: white; font-size: 16px; font-weight: bold;
            }
            QPushButton:hover { background-color: #5AA0F2; }
            QPushButton:pressed { background-color: #3A80D2; }
        """)
        self.button.clicked.connect(self.generate_qr)
        layout.addWidget(self.button)

        # QR CODE
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setStyleSheet("margin-top: 20px;")
        layout.addWidget(self.qr_label)

        self.setLayout(layout)

    def generate_qr(self):
        data = self.input.text().strip()

        if not data:
            QMessageBox.warning(self, "Aviso", "Digite algum conteúdo.")
            return

        try:
            # 1. Cria a base do QR Code
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(data)
            qr.make(fit=True)

            # 2. Gera a imagem
            img = qr.make_image(fill_color="black", back_color="white")

            # 3. Salva na Memória (Buffer) 
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")

            # 4. Exibe na interface
            qimage = QImage.fromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qimage)

            pixmap = pixmap.scaled(
                300, 300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self.qr_label.setPixmap(pixmap)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar a imagem:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeApp()
    window.show()
    sys.exit(app.exec())
