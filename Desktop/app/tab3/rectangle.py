from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PySide6.QtGui import QPen, QBrush, QColor, QFont


class RectangleItem(QGraphicsItem):
    """Custom item representing a rectangle with an index."""

    def __init__(self, rect, index, id):
        super().__init__()
        self.rect = rect
        self.index = index
        self.id = id
        self.text_item = QGraphicsTextItem(str(index))
        self.text_item.setDefaultTextColor(QColor(255, 255, 255))
        self.text_item.setFont(QFont("Arial", 10))
        self.update_text_position()

        self.pen = QPen(QColor(0, 255, 0), 2)
        self.brush = QBrush(QColor(0, 0, 255, 50))
        self.is_selected = False

        self.setTransformationOrigin()

    def boundingRect(self):
        margin = 2
        return self.rect.adjusted(-margin, -margin, margin, margin)

    def paint(self, painter, option, widget=None):
        pen_color = QColor(255, 0, 0) if self.is_selected else QColor(0, 255, 0)
        painter.setPen(QPen(pen_color, 2))
        painter.setBrush(self.brush)
        painter.drawRect(self.rect)

    def setSelected(self, is_selected):
        self.is_selected = is_selected
        self.update()

    def setTransformationOrigin(self):
        center_point = self.rect.center()
        self.setTransformOriginPoint(center_point)

    def update_text_position(self):
        center_point = self.rect.center()
        self.text_item.setPos(center_point.x() - 10, center_point.y() - 10)

    def set_index(self, new_index):
        self.index = new_index
        self.text_item.setPlainText(str(new_index))
        self.update_text_position()

    def move_by(self, dx, dy):
        self.prepareGeometryChange()
        self.rect.translate(dx, dy)
        self.update_text_position()
        self.setTransformationOrigin()
        self.update()
