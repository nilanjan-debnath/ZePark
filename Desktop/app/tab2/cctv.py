import time
import cv2
import numpy as np
import logging

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QObject, Signal, Slot, QThread, QSize
from PySide6.QtGui import QPixmap, QImage

from .frame_process import current_frames, processed_frames, frame_lock, processed_lock


class FrameReader(QObject):
    frameReady = Signal(np.ndarray)
    errorOccurred = Signal(str)
    readerStopped = Signal()

    def __init__(self, index: int, video_path: str, target_fps: int = 30):
        super().__init__()
        self.index = index
        self.video_path = video_path
        self._running = False
        self.cap = None
        self.target_delay = 1.0 / target_fps if target_fps > 0 else 0

    @Slot()
    def run(self):
        self._running = True
        logging.info(f"FrameReader [{self.index}]: Starting for {self.video_path}")
        self.cap = cv2.VideoCapture(self.video_path)

        if not self.cap.isOpened():
            error_msg = f"Error: Could not open video source {self.video_path}"
            logging.info(f"FrameReader [{self.index}]: {error_msg}")
            self.errorOccurred.emit(error_msg)
            self._running = False
            self.readerStopped.emit()
            return

        while self._running:
            start_time = time.time()
            try:
                ret, frame = self.cap.read()
                if ret:
                    self.frameReady.emit(frame)
                elif self.cap.isOpened():
                    logging.info(
                        f"FrameReader [{self.index}]: End of stream, looping..."
                    )
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                else:
                    logging.info(
                        f"FrameReader [{self.index}]: Read error or stream closed."
                    )
                    self._running = False
                    break

                elapsed_time = time.time() - start_time
                sleep_time = self.target_delay - elapsed_time
                if sleep_time > 0:
                    time.sleep(sleep_time)

            except Exception as e:
                error_msg = f"Error during frame read/emit: {e}"
                logging.info(f"FrameReader [{self.index}]: {error_msg}")
                self.errorOccurred.emit(error_msg)
                time.sleep(1)

        if self.cap and self.cap.isOpened():
            self.cap.release()
        logging.info(f"FrameReader [{self.index}]: Releasing capture and stopping.")
        self.readerStopped.emit()

    @Slot()
    def stop(self):
        """Signals the reading loop to stop."""
        logging.info(f"FrameReader [{self.index}]: Stop requested.")
        self._running = False


class CCVTPlayer(QWidget):
    def __init__(self, index: int, video_path: str):
        super().__init__()
        self.index = index
        self.video_path = video_path
        self.last_processed_pixmap = None  # Cache the last pixmap to reduce conversions

        self.init_ui()

        self.thread = QThread(self)
        self.reader = FrameReader(self.index, self.video_path)
        self.reader.moveToThread(self.thread)

        self.thread.started.connect(self.reader.run)
        self.reader.frameReady.connect(self.handleFrame)
        self.reader.errorOccurred.connect(self.handleError)

        self.reader.readerStopped.connect(self.thread.quit)
        self.reader.destroyed.connect(self.thread.quit)
        # Optional: Wait for thread to finish gracefully if needed
        self.thread.finished.connect(self.onThreadFinished)

        self.thread.start()

        logging.info(f"CCVTPlayer [{self.index}]: Initialized and thread started.")

    def init_ui(self):
        self.video_label = QLabel("Initializing Stream...")
        self.video_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.video_label)
        self.setLayout(layout)
        self.setMinimumSize(160, 90)

    @Slot(np.ndarray)
    def handleFrame(self, frame_bgr):
        if frame_bgr is None or not hasattr(self, "index"):
            return

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        with frame_lock:
            current_frames[self.index] = frame_rgb

        processed_frame_rgb = None
        with processed_lock:
            processed_frame_rgb = processed_frames.get(self.index, None)

        if processed_frame_rgb is not None:
            try:
                h, w, ch = processed_frame_rgb.shape
                if h > 0 and w > 0:
                    bytes_per_line = ch * w
                    q_image = QImage(
                        processed_frame_rgb.data,
                        w,
                        h,
                        bytes_per_line,
                        QImage.Format_RGB888,
                    )
                    # Create a persistent copy for the pixmap to avoid issues with underlying buffer changes
                    q_image_copy = q_image.copy()
                    self.last_processed_pixmap = QPixmap.fromImage(q_image_copy)

                    # Display the pixmap, scaled to the label's size
                    current_size = self.video_label.size()
                    if not current_size.isEmpty():
                        scaled_pixmap = self.last_processed_pixmap.scaled(
                            current_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                        self.video_label.setPixmap(scaled_pixmap)
                    else:  # Fallback if size is somehow zero
                        self.video_label.setPixmap(self.last_processed_pixmap)

            except Exception as e:
                logging.info(
                    f"CCVTPlayer [{self.index}]: Error converting processed frame to QPixmap: {e}"
                )
                self.video_label.clear()
                self.video_label.setText("Display Error")

    @Slot(str)
    def handleError(self, error_message):
        """Displays an error message on the video label."""
        logging.info(f"CCVTPlayer [{self.index}]: Received error: {error_message}")
        self.video_label.setText(error_message)
        # Consider stopping the reader/thread on critical errors
        self.reader.stop()

    def get_current_frame_pixmap(self, processed: bool = True) -> QPixmap | None:
        frame_rgb = None
        if processed:
            if self.last_processed_pixmap and not self.last_processed_pixmap.isNull():
                return self.last_processed_pixmap.copy()
            else:
                with processed_lock:
                    frame_rgb = processed_frames.get(self.index, None)
        else:
            with frame_lock:
                frame_rgb = current_frames.get(self.index, None)

        if frame_rgb is not None:
            try:
                h, w, ch = frame_rgb.shape
                if h > 0 and w > 0:
                    bytes_per_line = ch * w
                    q_image = QImage(
                        frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888
                    )
                    return QPixmap.fromImage(q_image.copy())
            except Exception as e:
                logging.info(
                    f"CCVTPlayer [{self.index}]: Error converting frame_rgb to QPixmap in get_current_frame: {e}"
                )

        return None

    def set_video_size(self, width, height):
        if width <= 0 or height <= 0:
            return

        aspect_ratio = 16.0 / 9.0
        target_height = height
        target_width = int(target_height * aspect_ratio)

        # If calculated width exceeds available width, recalculate based on width
        if target_width > width:
            target_width = width
            target_height = int(target_width / aspect_ratio)

        # Ensure calculated dimensions are not zero
        target_width = max(1, target_width)
        target_height = max(1, target_height)

        new_size = QSize(target_width, target_height)
        if self.video_label.size() != new_size:
            self.video_label.setFixedSize(new_size)
            # Update pixmap scaling if needed (optional, handleFrame might cover it)
            if self.last_processed_pixmap and not self.last_processed_pixmap.isNull():
                scaled_pixmap = self.last_processed_pixmap.scaled(
                    new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.video_label.setPixmap(scaled_pixmap)

    @Slot()
    def onThreadFinished(self):
        logging.info(f"CCVTPlayer [{self.index}]: Reader thread finished.")

    def stop_reading(self):
        logging.info(f"CCVTPlayer [{self.index}]: Requesting reader stop...")
        if hasattr(self, "reader") and self.reader is not None:
            self.reader.stop()

    def closeEvent(self, event):
        logging.info(f"CCVTPlayer [{self.index}]: Close event triggered.")
        self.stop_reading()

        if hasattr(self, "thread") and self.thread is not None:
            logging.info(
                f"CCVTPlayer [{self.index}]: Quitting and waiting for thread..."
            )
            self.thread.quit()
            # Wait for thread to finish. Adjust timeout as needed.
            if not self.thread.wait(3000):  # Wait max 3 seconds
                logging.info(
                    f"CCVTPlayer [{self.index}]: Warning: Thread did not finish gracefully. Terminating."
                )
                self.thread.terminate()  # Force termination if necessary
            else:
                logging.info(f"CCVTPlayer [{self.index}]: Thread finished.")

        # Clean up references
        self.reader = None
        self.thread = None
        logging.info(f"CCVTPlayer [{self.index}]: Cleanup complete.")
        super().closeEvent(event)
