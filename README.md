# 일단 된 것은 practice(1)


# 버전 설명

- 일단 데이터가 너무 작아서 val_size높임 : 0.1, 기본값 0.005


1. v1 : 그냥 기본
2. v2 
    - num_epochs : 3
    - train/eval_steps : 10
    - 오히려 학습할 수록 loss증가
    - vram : 9122MiB 소모
3. v3
    - num_epochs : 5
    - learning_rate : 5e-7
    - gradient_accumulation_steps : 4
        - 데이터셋 자체가너무 작아 업뎃이 없음
    - loss가 큼...
    - 실패!
    - vram : 8936MiB 소모
4. v4
    - learning_rate : 5e-6
        - 여기서 조금 줄이면 더 좋을 듯 : train loss변동성이 큼
    - cut_off_len : 200, 대화 자체가 짧음
    - eval loss가 드디어 준다
    - eval loss가 줄어들고, train보다 작다 == 학습이 제대로 된것!
    - 근데 실수로 v3에 저장함


## 개선사항
1. 그 뭐고 데이터셋에 instruction을 포함시켜서, 응답 유무로 구분해야할 듯
2. qlora는 데이터셋이 3~5만개는 필요...
3. full은 1000개만 있어도 됨


### 항상 바꿀 것
- wandb_run_name : 버전별로 따로따로 -> Gemma2_Single_GPU_2
- push_to_hub : 근데, 이거 버전별로 저장하고싶은데
    - 그냥 젤 좋은 거만 저장
- output_dir : 버전별로 -> ./gemma2_singleGPU-v2
- 모델들은 바로 허깅페이스에 올리고, 여긴 지우는게 ㅇㅇ, 메모리 문제

# 파인튜닝
1. fine_tunning.ipynb 실패 : 뭐 됏다 안됏다 안됨 ㄴㄴ
2. Single_GPU_Practice.ipynb 성공할 거 같은데..! -> 결국 챗봇으로 이어지긴 힘듬= 실패
3. 추론실패 oom
4. fine_tunning2.ipynb : 뭔가 애매









### gemma2-mz
- train loss가 왔다갔다 함 = 학습이 제대로 되지 않음
    - learning rate를 높여야 할 듯
    - 돌릴 시간은 없음 ㅋ
- eval은 줄긴함
- 소요 시간 : 6h 30m
- vram : 8666MiB

- 데이터 공개로 안올리니까, 다운이 안됨;
    - 허깅페이스 로그인도 했는데


# unsloth
1. conda activate unsloth
    - python : 3.10


vllm api
1. cd /home/eardream2/Jun/Fine_TT에서 실행해야 함 -> 이유는 모름
