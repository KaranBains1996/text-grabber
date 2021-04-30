import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu, QAction, QSystemTrayIcon
import tkinter as tk
from PIL import ImageGrab
from win10toast import ToastNotifier
import pyperclip


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)

        # Set cursor as cross
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )

        self.toaster = ToastNotifier()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')

        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        # Undo cursor to pointer
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.ArrowCursor)
        )

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('capture.png')

        self.toaster.show_toast("Text Grabber", "Text copied to clipboard", threaded=True)
        pyperclip.copy('I grabbed him')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))
    app.setQuitOnLastWindowClosed(False)

    # Adding item on the menu bar
    tray = QSystemTrayIcon()
    tray.setIcon(QIcon("icon.png"))
    tray.setVisible(True)

    # Creating the options
    menu = QMenu()
    about_item = QAction("About")
    about_item.setIcon(QIcon("about.png"))
    menu.addAction(about_item)

    # To quit the app
    quit_item = QAction("Quit")
    quit_item.triggered.connect(app.quit)
    quit_item.setIcon(QIcon("quit.png"))
    menu.addAction(quit_item)

    # Adding options to the System Tray
    tray.setContextMenu(menu)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
