import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                               QComboBox, QFileDialog, QProgressBar, QTextEdit)
from PySide6.QtGui import QPixmap, QFont, QPainter, QColor,QIcon, QBrush
from PySide6.QtCore import Qt, QSize, QObject, Signal, QThread

from carving import Carver

class Worker(QObject):
    finished = Signal()
    progress = Signal(int)

    def run(self, disk):  
        carver = Carver(disk)
        carver.extractFiles()
        self.finished.emit()

class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap("background.jpg")  # Ensure this file exists

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        x = (self.width() - scaled_pixmap.width()) // 2
        y = (self.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)

class OnboardingScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Background
        self.bg_widget = BackgroundWidget(self)
        self.bg_widget.setFixedSize(800, 600)

        # DECRYPTIX Title
        title_label = QLabel("DECRYPTIX", self)
        title_font = QFont("Roboto", 56, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)

        # Tagline
        tagline_label = QLabel("Recover Your Data with Ease: Expert Btrfs & XFS File System Solutions!", self)
        tagline_font = QFont("Roboto", 16)
        tagline_label.setFont(tagline_font)
        tagline_label.setStyleSheet("color: #34495e;")
        tagline_label.setAlignment(Qt.AlignCenter)
        tagline_label.setWordWrap(True)

        # Get Started Button
        start_button = QPushButton("GET STARTED", self)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 25px;
                max-width: 250px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        start_button.clicked.connect(self.on_get_started)

        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(tagline_label)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        # Set layout alignments
        layout.setAlignment(Qt.AlignCenter)

    def on_get_started(self):
        self.parent().parent().switch_to_main_screen()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 255, 255))

        painter.drawRect(self.rect())

class MainApplicationScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)

        # Top section (existing controls)
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        # Disk selection
        disk_layout = QHBoxLayout()
        self.disk_label = QLabel("Selected Disk:")
        self.disk_button = QPushButton("Browse")
        self.disk_button.clicked.connect(self.browse_disk)
        disk_layout.addWidget(self.disk_label)
        disk_layout.addWidget(self.disk_button)
        top_layout.addLayout(disk_layout)

        # File format dropdown
        format_layout = QHBoxLayout()
        format_label = QLabel("File Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["All", "JPG", "PNG", "GIF", "PDF", "DOC"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        top_layout.addLayout(format_layout)

        # Recovery method
        method_layout = QHBoxLayout()
        method_label = QLabel("Recovery Method:")
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Quick Scan", "Deep Scan", "File Carving"])
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_combo)
        top_layout.addLayout(method_layout)

        # Start button
        self.start_button = QPushButton("Start Recovery")
        self.start_button.clicked.connect(self.start_recovery)
        top_layout.addWidget(self.start_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        top_layout.addWidget(self.progress_bar)

        main_layout.addWidget(top_widget)

        # Logging area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }
        """)
        main_layout.addWidget(self.log_area)

        # Apply styles
        self.setStyleSheet("""
            QLabel {
                font-family: 'Roboto';
                font-size: 14px;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #50C878;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00A36C;
            }
            QComboBox {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                min-width: 150px;
                background-color: white;
            }
            QProgressBar {
                border: 2px solid #3498db;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)

    def browse_disk(self):
        disk = QFileDialog.getOpenFileUrl(self, "Select Disk")
        if disk:
            self.disk_label.setText(f"Selected Disk: {disk[0].toLocalFile()}")
            self.log_message(f"Disk selected: {disk}")

    def start_thread(self, disk):
        self.thread = QThread()
        self.worker = Worker()

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(lambda: self.worker.run(disk))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.log_message("Recovery completed successfully!", "success")

    def start_recovery(self):
        disk = self.disk_label.text().replace("Selected Disk: ", "")
        file_format = self.format_combo.currentText()
        method = self.method_combo.currentText()

        if not disk or disk == "Selected Disk:":
            self.log_message("Please select a disk first", "error")
            return

        self.log_message(f"Starting recovery: {file_format} files from {disk} using {method}")
        self.start_thread(disk)

    def log_message(self, message, level="info"):
        color = "#2c3e50"  # Default color (dark gray)
        if level == "error":
            color = "#e74c3c"  # Red for errors
        elif level == "success":
            color = "#27ae60"  # Green for success

        self.log_area.append(f'<span style="color: {color};">{message}</span>')
        self.log_area.ensureCursorVisible()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 255, 255))

        painter.drawRect(self.rect())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Decryptix")
        self.setFixedSize(800, 600)

        # Create a stacked widget to hold both the onboarding screen and main application
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create and add the onboarding screen
        self.onboarding_screen = OnboardingScreen(self)
        self.stacked_widget.addWidget(self.onboarding_screen)

        # Create and add the main application screen
        self.main_app_screen = MainApplicationScreen(self)
        self.stacked_widget.addWidget(self.main_app_screen)

        # Start with the onboarding screen
        self.stacked_widget.setCurrentWidget(self.onboarding_screen)

    def switch_to_main_screen(self):
        self.stacked_widget.setCurrentWidget(self.main_app_screen)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 255, 255))

        painter.drawRect(self.rect())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load Roboto font
    QFont.insertSubstitution("Roboto", "Arial")
    icon = QIcon("favicon.jpg")
   
    
    window = MainWindow()
    window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec())