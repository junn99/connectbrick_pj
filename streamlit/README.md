Streamlit을 사용하여 웹 브라우저 상에서 대화형 챗봇을 구현하며,  `beomi/Llama-3-Open-Ko-8B` 모델을 파인튜닝하여 만든 `junn991/llama3-8b-1gpu-couple` 모델을 API로 활용함.

---

## 주요 기능

1. **Streamlit 기반 웹 UI 제공**  
   - `st.set_page_config`와 `st.title`을 통해 페이지 제목, 파비콘, 페이지 타이틀을 설정함.  
   - 사이드바에서 `max_tokens`와 `temperature` 값을 동적으로 조정할 수 있음.  
   - 대화 히스토리와 입력창, 전송 버튼을 제공하여 사용자와 챗봇 간의 대화를 구현함.  

2. **vLLM 서버 연동**  
   - `vllm_host = "http://localhost:8000"`로 설정된 API 서버를 통해 응답을 생성함.  
   - API는 `junn991/llama3-8b-1gpu-couple` 모델을 활용하며, 이는 사용자가 `beomi/Llama-3-Open-Ko-8B` 모델을 기반으로 파인튜닝한 결과임.  
   - JSON 포맷으로 모델 입력(prompt)과 파라미터(temperature, max_tokens 등)를 전달함.  

3. **토크나이저 사용**  
   - Hugging Face의 `AutoTokenizer`를 사용하여 토크나이징 및 Chat 템플릿 적용(`apply_chat_template`)을 수행함.  
   - `@st.cache_resource`를 사용하여 토크나이저를 캐싱, 성능을 향상시킴.  

4. **대화 상태 관리**  
   - `st.session_state.messages`로 대화 내역을 상태로 관리함.  
   - "대화내용 지우기" 버튼을 통해 대화 기록을 초기화할 수 있음.  

5. **응답 정제(clean_response)**  
   - 모델의 원문 응답에서 불필요한 태그를 제거하고, 의미 있는 첫 번째 문장만 추출해 사용자에게 깔끔한 응답을 제공함.  

---

## 파일 구조

```bash
.
├─ requirements.txt (예: 필요한 라이브러리)
└─ app.py (본 코드)
```

`app.py`는 README와 동일한 디렉토리에 배치되어야 함.

---

## 사전 준비

1. **Python 설치**  
   Python 3.9 이상의 버전을 권장함.

2. **필요한 패키지 설치**  
   ```bash
   pip install streamlit requests transformers
   ```
   추가로, `junn991/llama3-8b-1gpu-couple` 모델이 vLLM 서버에서 정상적으로 로드되어야 함.

3. **vLLM 서버 구동**  
   - 코드에서 `http://localhost:8000`로 vLLM API 서버가 실행 중이라고 가정함.  
   - API는 `junn991/llama3-8b-1gpu-couple` 모델을 사용하며, 이는 `beomi/Llama-3-Open-Ko-8B`를 파인튜닝한 모델임.  
   - vLLM 서버의 설정 및 실행 방법은 vLLM 공식 문서를 참조.  

---

## 실행 방법

1. **토크나이저 및 모델 준비**  
   `junn991/llama3-8b-1gpu-couple` 모델을 로컬 환경에서 다운로드하거나 Hugging Face Hub에서 활용할 수 있도록 설정해야 함.

2. **Streamlit 앱 실행**  
   ```bash
   streamlit run app.py
   ```
   위 명령어를 실행하면 로컬 호스트(`http://localhost:8501`)에서 앱이 실행됨. 
