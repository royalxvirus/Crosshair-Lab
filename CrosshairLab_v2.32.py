import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Crosshair(QtWidgets.QWidget):
    def __init__(self, parent=None, windowSize=24, penWidth=2, color=(50, 255, 50), design=1):
        QtWidgets.QWidget.__init__(self, parent)
        self.ws = windowSize
        self.resize(windowSize + 1, windowSize + 1)
        self.pen = QtGui.QPen(QtGui.QColor(*color))
        self.pen.setWidth(penWidth)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTransparentForInput)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center() + QtCore.QPoint(1, 1))
        self.design = design

    def setCrosshairProperties(self, windowSize, penWidth, color, design):
        self.ws = windowSize
        self.pen.setWidth(penWidth)
        self.pen.setColor(QtGui.QColor(*color))
        self.design = design
        self.resize(windowSize + 1, windowSize + 1)
        self.update()

    def paintEvent(self, event):
        ws = self.ws
        res = int(ws / 2)
        red = int(ws / 3)
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)

        if self.design == 1:  # Original design
            crosshairlength = 3
            painter.drawLine(res, 0, res, res - red)
            painter.drawLine(res, res + red + 1, res, ws)
            painter.drawLine(0, res, res - red, res)
            painter.drawLine(res + red, res, ws - 0.5, res)
        elif self.design == 2:  # Dot design (filled circle in the middle)
            painter.setBrush(self.pen.color())
            painter.drawEllipse(res - 2, res - 2, 4, 4)  # Draw a filled circle
        elif self.design == 3:  # Square design
            painter.drawRect(res - red, res - red, 2 * red, 2 * red)
        elif self.design == 4:  # Cross design
            painter.drawLine(0, res, ws, res)
            painter.drawLine(res, 0, res, ws)
        elif self.design == 5:  # Circle design
            painter.drawEllipse(res - red, res - red, 2 * red, 2 * red)
        elif self.design == 6:  # Triangle design
            polygon = QtGui.QPolygon()
            polygon << QtCore.QPoint(res, 0)
            polygon << QtCore.QPoint(0, ws)
            polygon << QtCore.QPoint(ws, ws)
            painter.drawPolygon(polygon)
        elif self.design == 7:  # X design (Changed from Star)
            painter.drawLine(0, 0, ws, ws)
            painter.drawLine(0, ws, ws, 0)
        elif self.design == 8:  # Diamond design
            diamond = QtGui.QPolygon()
            diamond << QtCore.QPoint(res, 0)
            diamond << QtCore.QPoint(0, res)
            diamond << QtCore.QPoint(res, 2 * res)
            diamond << QtCore.QPoint(2 * res, res)
            painter.drawPolygon(diamond)
        elif self.design == 9:  # Arrow design
            arrow = QtGui.QPolygon()
            arrow << QtCore.QPoint(res, 0)
            arrow << QtCore.QPoint(0, ws)
            arrow << QtCore.QPoint(res, res)
            arrow << QtCore.QPoint(ws, ws)
            painter.drawPolygon(arrow)
        elif self.design == 10:  # Hexagon design
            hexagon = QtGui.QPolygon()
            for i in range(6):
                angle = 60 * i
                x = res + red * QtCore.qCos(angle * 3.14159265359 / 180)
                y = res - red * QtCore.qSin(angle * 3.14159265359 / 180)
                hexagon.append(QtCore.QPoint(x, y))
            painter.drawPolygon(hexagon)

class CrosshairEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Crosshair Lab')
        self.setGeometry(100, 100, 400, 200)

        self.crosshair = None

        self.size_label = QtWidgets.QLabel('(0-100) Size:')
        self.size_input = QtWidgets.QLineEdit()  # Text box for size
        self.size_input.setValidator(QtGui.QIntValidator(1, 100))  # Allow only integers from 1 to 100
        self.size_input.setAlignment(QtCore.Qt.AlignCenter)

        self.width_label = QtWidgets.QLabel('(0-10) Width:')
        self.width_input = QtWidgets.QLineEdit()  # Text box for width
        self.width_input.setValidator(QtGui.QIntValidator(1, 100))  # Allow only integers from 1 to 100
        self.width_input.setAlignment(QtCore.Qt.AlignCenter)

        self.color_label = QtWidgets.QLabel('Crosshair Color:')
        self.color_button = QtWidgets.QPushButton('Choose Color')
        self.color_button.clicked.connect(self.chooseColor)

        self.crosshair_design_label = QtWidgets.QLabel('Crosshair Theme:')
        self.crosshair_design_combo = QtWidgets.QComboBox()
        self.crosshair_design_combo.addItems(['Original', 'Dot', 'Square', 'Cross', 'Circle', 'Triangle', 'X', 'Diamond', 'Arrow', 'Exit'])

        self.apply_button = QtWidgets.QPushButton('Apply')
        self.apply_button.clicked.connect(self.applyChanges)

        self.save_button = QtWidgets.QPushButton('Save')
        self.save_button.clicked.connect(self.saveToFile)

        self.load_button = QtWidgets.QPushButton('Load Previous Crosshair')
        self.load_button.clicked.connect(self.loadPreviousCrosshair)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.size_label)
        self.layout.addWidget(self.size_input)
        self.layout.addWidget(self.width_label)
        self.layout.addWidget(self.width_input)
        self.layout.addWidget(self.color_label)
        self.layout.addWidget(self.color_button)
        self.layout.addWidget(self.crosshair_design_label)
        self.layout.addWidget(self.crosshair_design_combo)
        self.layout.addWidget(self.apply_button)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.load_button)  # Added the "Load Previous Crosshair" button
        self.setLayout(self.layout)

    def createCrosshair(self):
        if self.crosshair is not None:
            self.crosshair.close()
        windowSize = int(self.size_input.text())
        penWidth = int(self.width_input.text())
        color = self.color_button.palette().button().color().getRgb()[:-1]
        design_index = self.crosshair_design_combo.currentIndex() + 1
        self.crosshair = Crosshair(windowSize=windowSize, penWidth=penWidth, color=color, design=design_index)
        self.crosshair.show()

    def chooseColor(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.color_button.setStyleSheet("background-color: %s;" % color.name())

    def applyChanges(self):
        self.createCrosshair()

    def saveToFile(self):
        try:
            windowSize = int(self.size_input.text())
            penWidth = int(self.width_input.text())
            color = self.color_button.palette().button().color().getRgb()[:-1]
            design_index = self.crosshair_design_combo.currentIndex() + 1

            with open('crosshair_settings.txt', 'w') as file:
                file.write(f"Size: {windowSize}\n")
                file.write(f"Width: {penWidth}\n")
                file.write(f"Color: {', '.join(map(str, color))}\n")
                file.write(f"Design: {design_index}\n")
            print("Settings saved to crosshair_settings.txt")
        except ValueError:
            print("Invalid numeric values. Please enter valid values for Size and Width.")

    def loadPreviousCrosshair(self):
        try:
            with open('crosshair_settings.txt', 'r') as file:
                settings = {}
                for line in file:
                    parts = line.strip().split(': ')
                    if len(parts) == 2:
                        key, value = parts
                        settings[key] = value
                    else:
                        print("Invalid line format in the file:", line)

                # Check if all required settings are present
                if 'Size' in settings and 'Width' in settings and 'Color' in settings and 'Design' in settings:
                    try:
                        size = int(settings['Size'])
                        width = int(settings['Width'])
                        color = tuple(map(int, settings['Color'].split(', ')))
                        design_index = int(settings['Design'])

                        if 1 <= size <= 100 and 1 <= width <= 100:
                            self.size_input.setText(str(size))
                            self.width_input.setText(str(width))
                            self.color_button.setStyleSheet("background-color: rgb({}, {}, {});".format(*color))
                            self.crosshair_design_combo.setCurrentIndex(design_index - 1)

                            self.createCrosshair()
                        else:
                            print("Invalid size or width value in the file.")
                    except ValueError:
                        print("Invalid numeric values in the file.")
                else:
                    print("Missing required settings in the file.")
        except FileNotFoundError:
            print("No previous crosshair settings found.")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #2E2E2E;
            color: #EAEAEA;
            font-family: Arial, sans-serif;
        }
        QLabel {
            font-size: 12px;
        }
        QPushButton {
            background-color: #007ACC;
            border: 1px solid #007ACC;
            color: #FFFFFF;
            border-radius: 5px;
            padding: 5px 10px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #005B9F;
            border: 1px solid #005B9F;
        }
        QComboBox {
            background-color: #FFFFFF;
            color: #000000;
            border: 1px solid #CCCCCC;
            padding: 5px;
        }
    """)
    editor = CrosshairEditor()
    editor.show()
    sys.exit(app.exec_())
