import sys
import os
import csv
from datetime import datetime
import cv2
import numpy as np
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QThread, pyqtSignal, Qt

import torch
import pathlib

sys.modules["pathlib._local"] = pathlib 
if os.name == 'nt':
   pathlib.PosixPath = pathlib.WindowsPath
else:
   pathlib.WindowsPath = pathlib.PosixPath

# UI 파일 로드
form_class, _ = uic.loadUiType("./res/mainWin.ui")

path = ".\\best.pt"
model = torch.hub.load("./yolov5", "custom", path, source="local")

class CameraThread(QThread):
    frameCaptured = pyqtSignal(np.ndarray)
    
    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.latest_frame = None

    def run(self):
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                # Perform detection
                results = model(frame)
                detections = results.xyxy[0].cpu().numpy()  # Get detections

                # Draw bounding boxes and labels
                for *xyxy, conf, cls in detections:
                    x1, y1, x2, y2 = map(int, xyxy)
                    label = f"{model.names[int(cls)]} {conf:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                self.latest_frame = frame  # 마지막 캡처된 프레임 저장
                self.frameCaptured.emit(frame)
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

    def get_latest_frame(self):
        return self.latest_frame


class MyForm(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.camera_thread = CameraThread()
        self.camera_thread.frameCaptured.connect(self.update_frame)
        self.camera_thread.start()

        self.btnSave.clicked.connect(self.capture_image)

    def update_frame(self, frame):
        qt_img = self.convert_cv_to_qt(frame)
        self.webcam.setPixmap(qt_img)

    def convert_cv_to_qt(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_qt_format.scaled(self.webcam.size(), Qt.AspectRatioMode.IgnoreAspectRatio)
        return QPixmap.fromImage(p)

    def capture_image(self):
        name = 'pothole'

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.jpg"

        folder = "photo"
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)  # 폴더 생성
                print(f"폴더 '{folder}'가 생성되었습니다.")
            except Exception as e:
                print(f"폴더 생성 실패: {e}")
                return

        file_path = os.path.join(folder, filename)
        print(f"저장할 파일 경로: {file_path}")

        frame = self.camera_thread.get_latest_frame()  # 최신 프레임 가져오기
        if frame is not None:
            try:
                if cv2.imwrite(file_path, frame):  # 이미지 저장 시도
                    self.textView.setText(f"사진 저장 완료 {file_path}") #text(f"사진 저장 완료({file_path})")
                    print(f"사진 저장 완료: {file_path}")
                else:
                    print("사진 저장 실패: cv2.imwrite 실패")
            except Exception as e:
                print(f"사진 저장 중 오류 발생: {e}")
        else:
            print("프레임을 캡처할 수 없습니다.")

    def closeEvent(self, event):
        self.camera_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyForm()
    window.setWindowTitle("Pothole")
    window.show()
    sys.exit(app.exec())
