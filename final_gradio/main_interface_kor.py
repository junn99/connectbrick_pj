import json
import os
import time
import random
import gradio as gr
import numpy as np
import requests
from PIL import Image
import shutil
from datetime import datetime

# ComfyUI 경로
URL = "http://localhost:5001/api/prompt"
COMFY_OUTPUT_DIR = "/home/eardream2/ComfyUI/output"
COMFY_INPUT_DIR = "/home/eardream2/ComfyUI/input"

# 저장할 경로
INPUT_SAVE_DIR = "/home/eardream2/Jun/input"   
OUTPUT_SAVE_DIR = "/home/eardream2/Jun/output"
SAVED_IMAGES_DIR = "/home/eardream2/Jun/saved"

# 기본 프롬프트 설정
BASE_PROMPT = "professional portrait, studio lighting, neutral background, confident expression, clean and polished look, well-groomed hair, half body, front view, focus on face, slight exposure correction, sharp focus, highly detailed, 4k, high resolution, center"
BASE_NEGATIVE = "ac_neg1, pointed chin, nevus, beard, naked, big ears, nude, naked, exposed body, bare skin, revealing clothes, suggestive, explicit, stain, ink, trouble, flip out, baby hair, flyaway, cross-eyed, strabismus"

def ensure_directory(directory):
    """디렉토리가 없으면 생성"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def save_image(image_path):
    """이미지를 saved 폴더에 저장"""
    if not image_path:
        return "저장할 이미지가 없습니다"
    
    ensure_directory(SAVED_IMAGES_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_path = os.path.join(SAVED_IMAGES_DIR, f"saved_{timestamp}.png")
    
    try:
        shutil.copy(image_path, saved_path)
        return f"이미지가 성공적으로 저장되었습니다: {saved_path}"
    except Exception as e:
        return f"이미지 저장 실패: {str(e)}"

def get_saved_images():
    """저장된 이미지 목록 가져오기"""
    ensure_directory(SAVED_IMAGES_DIR)
    image_files = []
    for file in os.listdir(SAVED_IMAGES_DIR):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_files.append(os.path.join(SAVED_IMAGES_DIR, file))
    return sorted(image_files, key=os.path.getctime, reverse=True)

def combine_prompts(base_prompt, additional_prompt):
    """기본 프롬프트와 추가 프롬프트를 결합"""
    if additional_prompt.strip():
        return f"{base_prompt}, {additional_prompt}"
    return base_prompt

def get_gender_prompt(gender_option):
    """성별에 따른 프롬프트 반환"""
    return "an woman" if gender_option == "woman" else "a man"

def start_queue(prompt_workflow):
    """ComfyUI API에 작업 요청"""
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data=data)

def generate_image(
    input_image,
    additional_prompt,
    additional_negative,
    steps,
    denoise,
    instantid_weight,
    seed,
    seed_option,
    gender_option,
    age_option,
    resolution,
    instantid_start_at,
    instantid_end_at,
    pulid_weight,
    pulid_start_at,
    pulid_end_at,
    face_mask_blur,
    face_mask_padding,
    face_mask_expand
):   
    try:
        # 저장 디렉토리 확인
        ensure_directory(INPUT_SAVE_DIR)
        ensure_directory(OUTPUT_SAVE_DIR)
        
        # ComfyUI 출력 디렉토리 정리
        for file in os.listdir(COMFY_OUTPUT_DIR):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                os.remove(os.path.join(COMFY_OUTPUT_DIR, file))
        
        # 입력 이미지 처리 및 저장
        image = Image.fromarray(input_image)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_save_path = os.path.join(INPUT_SAVE_DIR, f"input_{timestamp}.png")
        image.save(input_save_path)
        print(f"입력 이미지 저장 위치: {input_save_path}")
        
        # ComfyUI 처리를 위한 리사이징
        min_side = min(image.size)
        scale_factor = 1024 / min_side
        new_size = (round(image.size[0] * scale_factor), round(image.size[1] * scale_factor))
        resized_image = image.resize(new_size)
        
        # ComfyUI input에 저장
        comfy_input_path = os.path.join(COMFY_INPUT_DIR, "test_api.jpg")
        resized_image.save(comfy_input_path)
        
        # 연령대별 프롬프트 매핑
        age_prompts = {
            "유아": "young child, baby face, innocent look, soft features, 3-6 years old",
            "청소년": "teenager, young face, youthful features, 13-19 years old",
            "중년": "middle aged, mature features, professional look, 40-55 years old",
            "노년": "elderly, senior, aged features, dignified look, over 60 years old"
        }
        
        # 워크플로우 설정
        with open("1112_PuLID_InstantID_swap_workflow.json", "r") as file_json:
            workflow = json.load(file_json)
        
        # 해상도 설정
        width, height = map(int, resolution.split('x'))
        workflow["45"]["inputs"].update({
            "width": width,
            "height": height
        })
        
        # 성별 프롬프트 생성
        gender_prompt = get_gender_prompt(gender_option)
        
        # 프롬프트 결합 (성별 프롬프트를 맨 앞에 배치)
        age_prompt = age_prompts.get(age_option, "")
        suit_type = "women's suit" if gender_option == "woman" else "formal suit"
        final_prompt = f"{gender_prompt},{suit_type}, {BASE_PROMPT}"
        if age_prompt:
            final_prompt = f"{final_prompt}, {age_prompt}"
        if additional_prompt.strip():
            final_prompt = f"{final_prompt}, {additional_prompt}"
            
        final_negative = combine_prompts(BASE_NEGATIVE, additional_negative)
        
        # 시드 설정
        actual_seed = seed if seed_option == "fixed" else random.randint(1, 1500000)
        workflow["49"]["inputs"].update({
            "seed": actual_seed,
            "steps": steps,
            "denoise": denoise,
        })
        
        # 프롬프트 업데이트
        workflow["42"]["inputs"]["text"] = final_prompt
        workflow["41"]["inputs"]["text"] = final_negative
        workflow["2"]["inputs"]["text"] = final_negative
        
        # 젠더 설정
        workflow["26"]["inputs"]["preset_expr"] = "#Female > #Male" if gender_option == "woman" else "#Female < #Male"
        
        # InstantID 파라미터 업데이트
        workflow["58"]["inputs"].update({
            "weight": instantid_weight,
            "start_at": instantid_start_at,
            "end_at": instantid_end_at
        })
        
        # PuLID 파라미터 업데이트
        workflow["75"]["inputs"].update({
            "weight": pulid_weight,
            "start_at": pulid_start_at,
            "end_at": pulid_end_at
        })
        
        # 페이스 마스크 파라미터 업데이트
        workflow["59"]["inputs"]["amount"] = face_mask_blur
        workflow["43"]["inputs"]["padding"] = face_mask_padding
        workflow["63"]["inputs"]["expand"] = face_mask_expand
        
        # 이미지 생성 시작
        start_time = time.time()
        start_queue(workflow)
        
        # 결과 대기 (최대 5분)
        max_wait = 300  # 5분
        found = False
        while time.time() - start_time < max_wait:
            time.sleep(5)  # 5초마다 체크
            
            # ComfyUI 출력 디렉토리에서 생성된 이미지 찾기
            output_files = [f for f in os.listdir(COMFY_OUTPUT_DIR) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            if output_files:
                print(f"출력 파일 발견: {int(time.time() - start_time)}초 소요")
                found = True
                break
            else:
                print(f"대기 중... ({int(time.time() - start_time)}초 경과)")
        
        if found and output_files:
            comfy_output_path = os.path.join(COMFY_OUTPUT_DIR, output_files[0])
            # 결과물 저장
            output_save_path = os.path.join(OUTPUT_SAVE_DIR, f"output_{timestamp}.png")
            shutil.copy(comfy_output_path, output_save_path)
            print(f"출력 이미지 저장 위치: {output_save_path}")
            print(f"사용된 시드 값: {actual_seed}")
            
            # ComfyUI 출력 디렉토리 정리
            for file in output_files:
                try:
                    os.remove(os.path.join(COMFY_OUTPUT_DIR, file))
                except Exception as e:
                    print(f"파일 제거 실패: {e}")
            
            return output_save_path
            
        raise Exception(f"{max_wait}초 대기 후에도 생성된 이미지를 찾을 수 없습니다")
        
    except Exception as e:
        print(f"이미지 생성 중 오류 발생: {str(e)}")
        raise gr.Error(f"이미지 생성 실패: {str(e)}")

def create_main_interface():
    """메인 인터페이스 생성"""
    with gr.Blocks() as main_interface:
        # 주의사항 추가
        with gr.Row():
            gr.Markdown("""
                ### ⚠️ 주의사항
                1. **정면 사진 권장**
                   - 정면을 응시하는 사진을 넣어주세요
                   - 측면 사진도 가능하나, 정면으로 변환 시 얼굴 형태가 훼손될 수 있습니다
                
                2. **화질**
                   - 가급적 고화질 사진을 제공해주세요
                   - 저화질도 생성 가능하나 결과물의 품질이 저하될 수 있습니다
                
                3. **얼굴 형태**
                   - 얼굴의 형태가 잘 드러나는 사진을 넣어주세요
                   - 일부가 가려진 사진도 생성 가능하나 결과물이 부자연스러울 수 있습니다
                
                4. **단일 인물**
                   - 생성이 필요한 분의 얼굴만 드러나야 합니다
                   - 다른 얼굴이 있다면 반드시 마스킹 처리해주세요
            """)
        
        with gr.Row():
            # 왼쪽 컬럼 - 기본 입력
            with gr.Column(scale=1):
                input_image = gr.Image(label="입력 이미지")
                
                with gr.Row():
                    gender = gr.Radio(
                        label="성별",
                        choices=["man", "woman"],
                        value="man",
                        type="value"
                    )
                    age = gr.Radio(
                        label="연령대",
                        choices=["유아", "청소년", "중년", "노년"],
                        value="노년"
                    )
                
                additional_prompt = gr.Textbox(
                    label="추가 프롬프트 (선택사항)",
                    placeholder="원하는 추가 프롬프트를 입력하세요...",
                    value=""
                )
                additional_negative = gr.Textbox(
                    label="추가 네거티브 프롬프트 (선택사항)",
                    placeholder="원하는 추가 네거티브 프롬프트를 입력하세요...",
                    value=""
                )
                
                with gr.Accordion("기본 프롬프트 (참고용)", open=False):
                    gr.Markdown(f"**기본 프롬프트:**\n{BASE_PROMPT}")
                    gr.Markdown(f"**기본 네거티브 프롬프트:**\n{BASE_NEGATIVE}")
                
                resolution = gr.Radio(
                    label="출력 해상도",
                    choices=["1024x1024", "1216x832", "832x1216"],
                    value="1024x1024"
                )
                
                steps = gr.Slider(label="스텝 수", minimum=1, maximum=100, step=1, value=10)
                denoise = gr.Slider(label="디노이즈 강도", minimum=0.8, maximum=1, step=0.05, value=0.9)
                
                with gr.Row():
                    seed_option = gr.Radio(
                        label="시드 모드",
                        choices=["random", "fixed"],
                        value="random",
                        interactive=True
                    )
                    seed = gr.Number(
                        label="고정 시드 값", 
                        value=-1,
                        interactive=True,
                        visible=False
                    )

            # 오른쪽 컬럼 - 출력 및 고급 설정
            with gr.Column(scale=1):
                output_image = gr.Image(label="출력 이미지")
                
                with gr.Row():
                    save_btn = gr.Button("💾 이미지 저장", variant="secondary")
                    save_status = gr.Textbox(label="저장 상태", interactive=False)
                
                with gr.Accordion("고급 설정", open=False):
                    gr.Markdown("### ID 모델 제어")
                    instantid_weight = gr.Slider(label="InstantID 가중치", minimum=0, maximum=2, step=0.1, value=1.2)
                    with gr.Row():
                        instantid_start_at = gr.Slider(label="시작", minimum=0, maximum=1, step=0.1, value=0)
                        instantid_end_at = gr.Slider(label="종료", minimum=0, maximum=1, step=0.1, value=1)
                    
                    gr.Markdown("### PuLID 제어")
                    pulid_weight = gr.Slider(label="PuLID 가중치", minimum=0, maximum=2, step=0.1, value=1)
                    with gr.Row():
                        pulid_start_at = gr.Slider(label="시작", minimum=0, maximum=1, step=0.1, value=0)
                        pulid_end_at = gr.Slider(label="종료", minimum=0, maximum=1, step=0.1, value=0.9)
                    
                    gr.Markdown("### 얼굴 마스크 제어")
                    face_mask_blur = gr.Slider(label="마스크 블러", minimum=0, maximum=128, step=1, value=64)
                    with gr.Row():
                        face_mask_padding = gr.Slider(label="패딩", minimum=0, maximum=300, step=10, value=50)
                        face_mask_expand = gr.Slider(label="확장", minimum=0, maximum=100, step=1, value=30)

        generate_btn = gr.Button("생성하기", variant="primary", size="lg")

        # 이벤트 연결
        def update_seed_visibility(mode):
            return gr.update(visible=(mode == "fixed"))

        seed_option.change(
            fn=update_seed_visibility,
            inputs=[seed_option],
            outputs=[seed]
        )

        generate_btn.click(
            fn=generate_image,
            inputs=[
                input_image, 
                additional_prompt,
                additional_negative,
                steps, denoise,
                instantid_weight, seed, seed_option,
                gender, age, resolution,
                instantid_start_at, instantid_end_at,
                pulid_weight, pulid_start_at, pulid_end_at,
                face_mask_blur, face_mask_padding, face_mask_expand
            ],
            outputs=output_image
        )

        save_btn.click(
            fn=save_image,
            inputs=[output_image],
            outputs=[save_status]
        )

    return main_interface

# 직접 실행시 테스트를 위한 코드
if __name__ == "__main__":
    # 필요한 디렉토리들 생성
    ensure_directory(INPUT_SAVE_DIR)
    ensure_directory(OUTPUT_SAVE_DIR)
    ensure_directory(SAVED_IMAGES_DIR)
    
    main_interface = create_main_interface()
    main_interface.launch(
        share=True,
        allowed_paths=[INPUT_SAVE_DIR, OUTPUT_SAVE_DIR, SAVED_IMAGES_DIR]
    )