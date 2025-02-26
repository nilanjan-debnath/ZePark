from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QColor
from PySide6.QtCore import QRectF


class MousePointerItem(QGraphicsItem):
    """Custom item to represent the mouse pointer."""

    def boundingRect(self):
        return QRectF(-5, -5, 10, 10)

    def paint(self, painter, option, widget=None):
        painter.setBrush(QColor(255, 0, 0))  # Red color
        painter.drawEllipse(self.boundingRect())
