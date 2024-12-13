# 사용법

### 0. ComfyUI 실행
ComfyUI가 실행 중인지 확인하세요.

### 1. Conda 환경 활성화
```bash
conda activate jun_web
```

### 2. 메인 애플리케이션 실행
```bash
python main_app.py
```

---

# 파일 구조

### 1. `main_app.py`
- Gradio 인터페이스를 실행하고 탭을 추가하는 역할을 합니다.

### 2. `main_interface_kor.py`
- 주요 로직과 핵심 기능이 포함되어 있습니다.

#### 주요 기능:
1. **경로 설정**
    - 로컬 호스트
    - ComfyUI
    - 입력/출력 디렉터리

2. **프롬프트 설정**
    - 기본 프롬프트 설정 (ComfyUI 워크플로우 업데이트 필요).
    - 추가 프롬프트 및 인터페이스 설정.

### 3. `llava_interface.py`
- 이미지 태그 기능을 처리합니다.

---

# 새로운 기능 추가

새로운 기능을 통합하려면 다음 단계를 따르세요:

### 1. 새 파일 생성

예: `new_feature.py`

```python
# new_feature.py

def create_new_feature():
    with gr.Blocks() as new_interface:
        # 새로운 기능의 UI를 구현하세요
        pass
    return new_interface
```

### 2. `main_app.py` 업데이트

1. 새로운 기능을 가져오기:

```python
from new_feature import create_new_feature
```

2. 새로운 인터페이스를 탭 목록에 추가:

```python
demo = gr.TabbedInterface(
    interface_list=[
        create_main_interface(),
        img2img_demo,
        txt_to_img,
        create_new_feature()  # 새로운 기능 추가
    ],
    tab_names=[
        "ID Photo Generator",
        "Image to Image",
        "Text to Image",
        "New Feature"  # 새로운 탭 이름
    ]
)
```
