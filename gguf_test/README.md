- 학습은 잘 되긴 함 : 근데? 데이터가 너무 작아서 그렇게 효과적이진 못한듯
- 추가적으로 modelfile에 따라서 성능이 확 갈린다
    - modelfile2가 제대로 적은 거 = 중복답변 사라짐

- llama3-8b-unsloth-q8:latest 모델도 답변이 영 별로다
- unsloth.Q8_0:latest : 막상 답변이 다 이상함, 애초에 일단 모델 파일이 잘못됨
-  뭔가 그냥 대화가 안되네 ㅋㅋ


- llama3-8b-stt-unsloth:latest
    - 확실히 좀 사람답게 대답함 : 그래도 조금 어색함
    - 확실히 데이터 질이 중요한듯
    - 음성(전화) 데이터 사용


llama3-couple:latest 이게 제일 자연스러움