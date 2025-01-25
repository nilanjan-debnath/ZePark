from point import MousePointerItem
from rectangle import RectangleItem
from background import Background
import json
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QInputDialog
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap
from PySide6.QtCore import Qt, QRectF, QPointF


class Canvas(QGraphicsView):
    """Main canvas for drawing and interacting with items."""

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMouseTracking(True)

        self.image_path = Background.image(0)
        self.pointer_item = None
        self.start_point = None
        self.temp_rect_item = None
        self.pre_save = []
        self.rectangles = []
        self.undo_stack = []
        self.selected_rectangle = None
        self.scale_factor = 1.0  # Zoom variable
        self.is_panning = False
        self.pan_start_position = QPointF()

        self.setFocusPolicy(Qt.StrongFocus)  # Enable Keyboard focus
        self.add_pointer()

    def add_pointer(self):
        self.pointer_item = MousePointerItem()
        self.scene.addItem(self.pointer_item)

    def mouseMoveEvent(self, event):
        scene_pos = self.mapToScene(event.position().toPoint())
        if self.is_panning:
            delta = scene_pos - self.mapToScene(self.pan_start_position.toPoint())
            self.pan_start_position = event.position()
            self.translate(-delta.x(), -delta.y())
        else:
            self.pointer_item.setPos(scene_pos)
            if self.start_point:
                rect = QRectF(self.start_point, scene_pos).normalized()
                if not self.temp_rect_item:
                    self.temp_rect_item = self.scene.addRect(
                        rect, QPen(QColor(0, 255, 0), 2, Qt.DashLine)
                    )
                else:
                    self.temp_rect_item.setRect(rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.is_panning = True
            self.pan_start_position = event.position()
            self.setCursor(Qt.ClosedHandCursor)
        elif event.button() == Qt.LeftButton:
            clicked_point = self.mapToScene(event.position().toPoint())
            self.start_point = clicked_point

            for rect_item in self.rectangles:
                if rect_item.boundingRect().contains(clicked_point):
                    self.select_rectangle(rect_item)
                    return
            self.clear_selection()

        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            clicked_point = self.mapToScene(event.position().toPoint())
            for rect_item in self.rectangles:
                if rect_item.boundingRect().contains(clicked_point):
                    new_index, ok = QInputDialog.getInt(
                        self.viewport(),
                        "Edit Rectangle Index",
                        f"Enter new index for rectangle {rect_item.index}:",
                        rect_item.index,
                        0,
                        len(self.rectangles) - 1,
                    )
                    if ok:
                        rect_item.set_index(new_index)
                    return

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.is_panning = False
            self.setCursor(Qt.ArrowCursor)
        elif event.button() == Qt.LeftButton and self.start_point:
            end_point = self.mapToScene(event.position().toPoint())
            rect = QRectF(self.start_point, end_point).normalized()

            if rect.width() > 0 and rect.height() > 0:
                self.add_rectangle(rect)
            if self.temp_rect_item:
                self.scene.removeItem(self.temp_rect_item)
                self.temp_rect_item = None
            self.start_point = None

    def add_rectangle(self, rect, rotation=0):
        rect_item = RectangleItem(rect, len(self.rectangles))
        self.scene.addItem(rect_item)
        self.scene.addItem(rect_item.text_item)
        self.rectangles.append(rect_item)
        rect_item.setRotation(rotation)
        self.update_button_states()

    def keyPressEvent(self, event):
        if self.selected_rectangle:
            dx, dy = 0, 0
            if event.key() == Qt.Key_Up:
                dy = -5
            elif event.key() == Qt.Key_Down:
                dy = 5
            elif event.key() == Qt.Key_Left:
                dx = -5
            elif event.key() == Qt.Key_Right:
                dx = 5

            self.selected_rectangle.move_by(dx, dy)

    def wheelEvent(self, event):
        if self.selected_rectangle:
            angle_change = 5
            rotation_angle = self.selected_rectangle.rotation() + (
                angle_change if event.angleDelta().y() > 0 else -angle_change
            )
            self.selected_rectangle.setRotation(rotation_angle)
        else:
            zoom_in = event.angleDelta().y() > 0
            factor = 1.1 if zoom_in else 0.9
            self.scale(factor, factor)

        super().wheelEvent(event)

    def select_rectangle(self, rect_item):
        if self.selected_rectangle == rect_item:
            return
        if self.selected_rectangle:
            self.selected_rectangle.setSelected(False)
        self.selected_rectangle = rect_item
        self.selected_rectangle.setSelected(True)

        self.update_button_states()

    def clear_selection(self):
        if self.selected_rectangle:
            self.selected_rectangle.setSelected(False)
            self.selected_rectangle = None

        self.update_button_states()

    def rect_to_json(self):
        self.reset_indexes()

        rectangle_data = [
            {
                "index": rect.index,
                "x": rect.rect.x() / self.width,
                "y": rect.rect.y() / self.height,
                "width": rect.rect.width() / self.width,
                "height": rect.rect.height() / self.height,
                "rotation": rect.rotation() % 360,
            }
            for rect in self.rectangles
        ]
        return rectangle_data

    def save(self):
        rectangle_data = self.rect_to_json()
        with open("rectangles.json", "w") as file:
            json.dump(rectangle_data, file, indent=4)

    def json_to_rect(self, rectangle_data):
        for rect in rectangle_data:
            self.add_rectangle(
                QRectF(
                    rect["x"] * self.width,
                    rect["y"] * self.height,
                    rect["width"] * self.width,
                    rect["height"] * self.height,
                ),
                rect["rotation"],
            )

    def load(self):
        try:
            with open("rectangles.json", "r") as file:
                rectangle_data = json.load(file)
            self.clear()
            self.json_to_rect(rectangle_data)
        except FileNotFoundError:
            print("No saved rectangles found.")

    def set_buttons(self, undo_button, redo_button, remove_button):
        self.undo_button = undo_button
        self.redo_button = redo_button
        self.remove_button = remove_button
        self.update_button_states()

    def update_button_states(self):
        if hasattr(self, "undo_button") and self.undo_button:
            self.undo_button.setEnabled(bool(self.rectangles))
        if hasattr(self, "redo_button") and self.redo_button:
            self.redo_button.setEnabled(bool(self.undo_stack))
        if hasattr(self, "remove_button") and self.remove_button:
            self.remove_button.setEnabled(bool(self.selected_rectangle))

    def undo(self):
        if self.rectangles:
            last_rectangle = self.rectangles.pop()
            self.undo_stack.append(last_rectangle)
            self.scene.removeItem(last_rectangle)
            self.scene.removeItem(last_rectangle.text_item)
            self.update_button_states()

    def redo(self):
        if self.undo_stack:
            restored_rectangle = self.undo_stack.pop()
            self.rectangles.append(restored_rectangle)
            self.scene.addItem(restored_rectangle)
            self.scene.addItem(restored_rectangle.text_item)
            self.update_button_states()

    def remove(self):
        if self.selected_rectangle:
            self.undo_stack.append(self.selected_rectangle)
            self.scene.removeItem(self.selected_rectangle)
            self.scene.removeItem(self.selected_rectangle.text_item)
            self.rectangles.remove(self.selected_rectangle)
            self.selected_rectangle = None
            self.reset_indexes()
            self.update_button_states()

    def clear(self):
        for rect_item in self.rectangles:
            self.undo_stack.append(rect_item)
            self.scene.removeItem(rect_item)
            self.scene.removeItem(rect_item.text_item)
        self.rectangles.clear()
        self.update_button_states()

    def reset_indexes(self):
        for index, rect_item in enumerate(self.rectangles):
            rect_item.set_index(index)

    def reset_view(self):
        self.resetTransform()
        self.scale_factor = 1.0
        self.centerOn(self.scene.sceneRect().center())

    def resize_canvas(self, width, height):
        """Resizes the canvas and sets the background image while maintaining a 16:9 aspect ratio."""
        # Calculate new dimensions to maintain 16:9 ratio
        self.pre_save = self.rect_to_json()
        self.width = width
        self.height = int(self.width / 16 * 9)

        if self.height > height:
            self.height = height
            self.width = int(self.height * 16 / 9)

        # Set the scene rectangle to match the calculated size
        self.scene.setSceneRect(0, 0, self.width, self.height)

        # Set the background image
        self.set_background_image()

    def set_background_image(self):
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                self.width,
                self.height,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation,
            )
            self.clear()
            self.scene.clear()
            self.scene.addPixmap(scaled_pixmap)
            self.add_pointer()
            self.json_to_rect(self.pre_save)
        else:
            print(f"Failed to load image: {self.image_path}")

    def update_background(self, image_path):
        self.image_path = image_path
        self.set_background_image()
