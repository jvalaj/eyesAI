import sys
import random
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QImage
from PIL import ImageGrab

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Overlay")
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.X11BypassWindowManagerHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()

        self.rectangles = []

        # Refresh every 500ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_overlay)
        self.timer.start(500)

    def update_overlay(self):
        # Take screenshot
        img = ImageGrab.grab()
        img_np = np.array(img.convert("RGB"))
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Threshold and find contours
        _, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.rectangles = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 50 and h > 20:  # Filter small noise
                color = QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                self.rectangles.append((x, y, w, h, color))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for x, y, w, h, color in self.rectangles:
            pen = QPen(color, 3)
            painter.setPen(pen)
            painter.drawRect(x, y, w, h)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = OverlayWindow()
    sys.exit(app.exec_())
