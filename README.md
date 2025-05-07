#  YOLOv5, PyQt6, Webcam을 이용한 포트홀 감지 프로그램 

이 프로젝트는 **YOLOv5**, **PyQt6**, 그리고 **웹캠**을 이용하여 도로 위의 **포트홀(pothole)** 을 실시간으로 탐지하고, UI에서 촬영 버튼을 눌러 현재 프레임을 저장하는 기능을 제공합니다. `pothole dataset`을 기반으로 학습된 모델(`best.pt`)을 사용합니다.

---
## dataset
    https://public.roboflow.ai/object-detection/pothole

## Yolov5
    https://github.com/ultralytics/yolov5

## 주요 기능

- YOLOv5를 이용한 **실시간 포트홀 탐지**
- PyQt6 기반의 **GUI 인터페이스**
- 웹캠 영상 스트리밍
- **촬영 버튼**을 누르면 현재 프레임을 `photo/` 폴더에 저장
- 저장된 이미지 경로를 GUI에 **텍스트로 표시**



![스크린샷 2025-05-07 122612](https://github.com/user-attachments/assets/af94a50a-d584-438e-aaed-7053545ab287)
