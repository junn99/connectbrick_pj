# 사용법
0. comfyui on
1. conda activate jun_web
2. python main_app.py


# 파일 구성
- main_app : Gradio 실행 & 탭 추가
- main_interface_kor : main 로직 및 주요 코드 구성
      1. 경로 설정
          - 로컬 호스트
          - ComfyUI
          - In/Output
      2. 기본 프롬프트 설정, comfyui workflow도 바꿔줘야 함.
          - 추가 프롬프트 설정
          - 인터페이스 설정
- llava_interface : 이미지 태그


# ----------------------새로운 기능을 추가하려면--------------------------------

새로운 파일 생성 (예: new_feature.py)
인터페이스 함수 구현
main_app.py에서 import하고 interface_list와 tab_names에 추가

예를 들어 새로운 기능을 추가할 때:
### new_feature.py
def create_new_feature():
    with gr.Blocks() as new_interface:
        # 새로운 기능의 UI 구현
        pass
    return new_interface

### main_app.py에 추가
from new_feature import create_new_feature

demo = gr.TabbedInterface(
    interface_list=[
        create_main_interface(),
        img2img_demo,
        txt_to_img,
        create_new_feature()    # 새로운 기능 추가
    ],
    tab_names=[
        "ID Photo Generator",
        "Image to Image",
        "Text to Image",
        "New Feature"          # 새로운 탭 이름
    ]
)
