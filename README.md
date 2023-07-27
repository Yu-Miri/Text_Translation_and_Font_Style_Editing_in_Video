# **Text Translation and Font Style Editing in Video**
## 웹사이트 시연
### 영상 업로드 및 텍스트 자동 편집 시연 영상
![영상 업로드 및 텍스트 자동 편집 영상](https://github.com/Yu-Miri/Text_Translation_and_Font_Style_Editing_in_Video/assets/121469490/5f78dfe5-e65a-460a-8e32-d6b5b03ff2e9)

### 텍스트 재생성 시연 영상
![웹사이트 시연 영상](https://github.com/Yu-Miri/Text_Translation_and_Font_Style_Editing_in_Video/assets/121469490/7b2d802e-5413-43fd-945d-172f0a57ba47)

### 텍스트 제거 시연 영상
![텍스트 제거 영상](https://github.com/Yu-Miri/Text_Translation_and_Font_Style_Editing_in_Video/assets/121469490/bae8168f-cce8-43c5-b8b2-8ae854c94fa8)

## 프로젝트 개요

- **기간** : 2023.04.24 ~ 2023.06.23
- **프로젝트 진행 인원** : 4명
- **주요 업무 및 상세 역할**
    - **Easy OCR** : 초기에 영상 내 텍스트는 문장 단위로 감지되어 문장의 번역과 번역된 텍스트에 폰트 스타일을 적용하는 이미지 생성에 문제가 발생했으며, 이를 해결하기 위해 모델 구조를 파악하여 단어 단위로 감지하도록 하이퍼 파라미터를 직접 조정하여 성능을 개선하였습니다.
    - **Mostel Train Dataset 생성** : 원본 이미지의 Text Font Style을 학습하여 Target Text에 Font Style Transfer를 적용하는 End-to-End 프레임워크 모델인 Mostel은 영어로만 사전 학습되었기에, 한국어 Text Font Style을 영어 Target Text에 Font Style을 적용시킬 수 없었습니다. 이를 해결하기 위해 해당 Task에 맞게 pygame 라이브러리를 사용하여 108개의 다양한 폰트와 16,000장의 배경 이미지로 350,000개의 한영 버전의 데이터셋을 구축하고, 준지도 학습에 필요한 현실 이미지 데이터셋 100,000개를 수집하여 성능을 개선하였습니다.
    - **Mostel Custom**
        - 기존 Mostel의 글자와 배경을 분리하는 모듈에서는 글자가 있는 영역을 감지하고 해당 영역에 대하여 이진화 된 Masking Image를 적용하여 마스크가 적용된 부분에 대해서만 글자를 제거하고 해당 영역이 아닌 부분의 배경을 보존하여 새로운 배경을 생성한 결과 Text의 테두리가 남는 문제가 발생하였습니다. 이를 해결하기 위해 Mostel의 구조 파악 후 Inpainting 모듈을 커스텀하여 글자 수정 영역을 넓히기 위해 글자 팽창 연산을 적용시킨 Masking Image를 학습하여 성능을 개선하였습니다.
        - Mostel의 글자를 재생성 하는 모듈에서는 글자를 인식할 수 있는 Recognizer를 사용하여 글자의 위치, 방향, 색상 등 원본 이미지의 글자에 대한 특징을 바꾸고자 하는 글자에 적용하여 글자가 지워진 배경 이미지와 Fusion하여 새로운 이미지를 생성하지만, 영어로만 학습되어 있기에 한국어 Font Style을 학습하지 못 하고 Target Text에 Font Style이 적용되지 않는 문제가 발생하였습니다. 이를 해결하기 위해 Mostel의 구조 파악 후 Recognizer 모듈을 커스텀하여 한국어와 영어 두 언어 모두 인식할 수 있도록 학습하여 성능을 개선하였습니다.
    - **Mostel Train** : 지도 학습에 쓰이는 생성한 합성 이미지 데이터셋과 준지도 학습에 쓰이는 현실 이미지 데이터셋을 7:1 Batch의 비율로 하여 학습을 진행하였으며, 정성적으로 Text Style Transfer 결과를 확인하면서 평가하고, 이에 더하여 정량적으로 Loss의 모니터링, Metrics를 통해 하이퍼 파라미터인 Learning Rate를 0.00005로 하여 15만 번의 학습을 진행한 후, 0.00004로 감소시켜 7만 번의 학습을 진행하였습니다.
    - **웹사이트 구축** : 웹사이트의 구상도 제작과 Flask를 통하여 전체적인 웹사이트의 디자인, 회원가입창, 로그인창, 편집기록창, 업로드창, 영상 업로드창을 구축하였습니다.
- **사용언어 및 개발환경** : AWS, VSCode, Ubuntu, MySQLWorkbench, FileZilla, Slack, Flask, Docker, Anaconda, Google colab Pro+, Python, Notion

---

## 문제 정의

- OTT 플랫폼을 통해 해외 콘텐츠 접근성이 올라가며, 국내 콘텐츠 수출 시장의 규모가 성장하는 추세로, 2021년 하반기 기준 콘텐츠 산업 수출이 전년 대비 13.9% 증가하는 것을 볼 수 있다.
<img width="566" alt="스크린샷 2023-07-09 오후 5 20 39" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/2951dbc0-d64c-4143-b5e9-5423c63d0031">

- 원작과 수출작을 비교해 보았을 때, 언어는 달라지지만 원작 스타일을 최대한 보존하여 수출되고 있다. 컴퓨터 그래픽 작업은 각 프레임 별로 편집자가 해당 영역에 대해 글자 뒤 배경의 손실을 최소화하고 새로운 글자로 편집하는 작업이 필요하지만, 이러한 작업은 10초 길이의 영상 기준으로 10만원에서 300만원 사이의 비용과 60초 이내의 영상 기준으로 최소 2일에서 5일 사이의 제작기간이 소요된다. 또한, 자동으로 번역하는 기술도 있지만 배경의 손실과 글자 스타일을 그대로 적용하기에 실제로 사용하기 어렵다.
<img width="571" alt="스크린샷 2023-07-09 오후 5 21 37" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/6eedf8d0-89fe-454a-98af-4bc424dc9cfb">

<img width="573" alt="스크린샷 2023-07-09 오후 5 22 26" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/885aeffc-f8ee-4f19-8c47-9bd4430f77fd">

- **실제 사례**
<img width="565" alt="스크린샷 2023-07-09 오후 5 22 58" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/1c3ff976-ca3d-4f7e-a03a-7f0c70e34676">
    
---
## 해결 방안

### <프로젝트 목적>

- OCR을 통해 영상 내 한국어 글자 이미지를 크롭하여 저장 후 GAN 계열의 딥러닝 모델을 통해 한국어 글자 스타일을 번역된 영어 글자에 적용시켜 시각적으로 일관성 있는 영어 글자 이미지를 생성하여 자연스럽게 편집된 영상을 제공하기 위해 GAN 계열 모델의 데이터셋을 커스텀화하여 Fine Tuning을 진행함으로서, 선정한 모델의 개선 및 웹사이트 제작을 경험
- 글자 뒤 배경 손실을 최소화하면서 자동으로 영상 내 글자를 편집하는 기능을 제공하여 시간과 비용을 절약할 수 있으며, 국내 콘텐츠의 수출 증가에 기여함과 동시에 컴퓨터 그래픽 작업의 기술에 대한 전문 지식이 없는 일반 사용자들에게 손쉽게 영상 내 글자 이미지 편집 도움

### <프로젝트 내용>

- 팀 프로젝트를 통하여 컴퓨터 그래픽 작업을 효율적으로 하기 위해 동영상을 프레임 단위의 이미지로 추출하는 기술, 광학문자인식(OCR), 번역기, 이미지 생성 모델인 MOSTEL 딥러닝 모델을 사용하여 영상 속에 등장하는 한국어를 영어로 바꾸어서 편집된 영상을 자동 및 수동으로 제작할 수 있는 웹사이트를 제공

### <“Text Translation and Font Style Editing in Video” 프로젝트의 End-to-End Framework 구조>
<img width="1232" alt="스크린샷 2023-07-09 오후 5 25 36" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/4f3735c4-1937-444b-8d4b-c934cdb6a72d">


- 본 프로젝트는 딥러닝 모델을 활용하여 영상 내 한국어 글자 스타일을 번역된 영어 글자에 적용하여 컴퓨터 그래픽을 자동으로 편집하는 End-to-End Framework 제시한다.

## 편집 영상
[원본 영상](https://youtu.be/X7MI3SjqPlc) : 영화 '베테랑' 한 장면

[자동 편집 영상](https://youtu.be/fayuC1aMplA) : 영상 내 텍스트 자동 번역 및 편집 영상 결과

[수동 편집 영상](https://youtu.be/r_7hRjK7z-Y) : 영상 내 텍스트 수동 번역 및 편집 영상 결과

[텍스트 제거 영상](https://youtu.be/GzN6uqkJaVw) : 영상 내 텍스트 제거 영상 결과

---
## 편집 프로그램 개요

1. 비디오 업로드 & 프레임 단위의 이미지 추출
2. 텍스트 감지 & 인식
3. 프레임 단위 번역 및 글자 스타일 적용
4. 변환된 프레임을 영상으로 재생성
---
## 영상 편집 방법

- AI를 활용한 영상 내 텍스트 자동 번역 및 편집 기능
- 영상 내 텍스트 수동 번역 및 편집 기능
- 영상 내 텍스트 제거 기능
---
## AI를 활용한 영상 내 텍스트 자동 번역 및 편집 기능

### 자동편집 개요

<img width="1255" alt="스크린샷 2023-07-09 오후 5 26 58" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/3eb5454b-5ce6-4937-b497-298e4403fc06">


1. **OCR & Crop** : 원본 영상 프레임 내 텍스트 영역을 감지 후 텍스트로 변환하여 텍스트 영역을 crop하여 저장
2. **Translation** : Helsinki-NLP 기반의 opus-mt-ko-en 모델을 통하여 자동으로 한영 번역
3. **Inpainting** : 글자를 제거한 배경 이미지 생성
4. **Font Style Transfer** : 번역된 텍스트에 OCR & Crop을 통해 저장된 텍스트 스타일 변환을 적용

### **OCR & Crop** : Easy OCR

- 광학문자인식 기술은 컴퓨터가 이미지 내 존재하는 글자들을 감지하여 글자의 영역을 표시해 주며, 감지한 글자의 내용을 추출하는 기능으로, 한국어를 영어로 번역할 때 한국어의 위치를 감지 및 인식하여 해당 영역을 잘라서 저장하며, 번역기를 통해 인식된 한국어를 영어로 변환할 때 사용한다.
- 기존에 문장 단위로 인식된 문제를 Easy OCR의 공식 문서를 파악하여 단어 단위로 인식하도록 하이퍼 파라미터를 조정하여 번역의 정확도를 높일 수 있었다.
- Easy OCR의 선정 이유 : 80가지 이상의 언어 인식이 가능하고, 한국어로 학습된 모델이 존재했으며, OCR 모델 중에서도 유명한 Tesseract에 비해 상대적으로 한국어 정확도가 높았기에 OCR의 모델을 Easy OCR으로 선정하였다.
<img width="882" alt="스크린샷 2023-07-09 오후 5 27 33" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/82f4d755-4d9e-4fea-b658-b13663061944">



### Translation : Papago API

- 영상 내 인식된 글자를 자동으로 번역
<img width="867" alt="스크린샷 2023-07-09 오후 5 28 17" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/4090c2a8-6527-443a-9826-5aedde883d66">


### **Inpainting & Font Style Transfer : MOSTEL**

**MOSTEL Architecture & Method**
<img width="858" alt="스크린샷 2023-07-09 오후 5 29 35" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/88653ddc-3b08-457e-b029-792662d68b72">



**BRM** : 배경에서 유지해야 하는 영역을 분할 및 보존하여 텍스트를 지워주는 모듈

**TMM** : 판독 불가능한 서체와 스타일을 추출하여 원본 이미지의 스타일을 학습하고 번역된 텍스트에 스타일을 적용하는 모듈

- 각각의 모듈은 3개의 Downsampling Layer 인코더와 3개의 Upsampling Layer 디코더로 구성
- **PSP**[Pyramid Scene Parsing]
    - 이미지의 크기를 [1, 2, 3, 6] 단위로 다르게 조정하여 하나의 입력 이미지에 대해서 다양한 크기를 학습하는 모듈
    - 모든 픽셀이 수정되면 배경 영역에 불필요한 변화가 발생되므로, 유지해야 하는 영역에 대해서만 수정
- **EG**[Editing Guidance]
    - 마스킹된 이미지를 통해 텍스트가 있는 부분의 위치정보를 저장해 변하지 않는 배경 영역과 텍스트 영역의 스타일을 명시하는 모듈
- **SLM**[Stroke Level Modification]
    - EG의 출력이 Stroke 영역의 분할 작업에 해당되며, 배경의 무결성을 위해 픽셀의 변화를 최소화하는 모듈
    - 마스킹 이미지를 통해 명시적으로 Editing Point를 Guide하여 안정적으로 편집 이미지를 생성

<img width="860" alt="스크린샷 2023-07-09 오후 5 29 57" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/7ccb2496-5c9a-425a-9d78-d8b661ea8208">

- **Pre-Transformation** : 원본 이미지와 타겟 텍스트 이미지를 부분적으로 특수한 변환을 적용시켜 전처리하고, Background Feature와 Text Style을 혼합하여 Edited Image를 생성하는 모듈
    - **Back Filtering** : 학습에 방해가 되는 복잡한 배경은 BRM에서 생성한 마스킹 이미지를 통해 배경을 필터링하여 노이즈 제거
    - **Style Augment** : 정확한 Text Style Generation을 위해 임의의 회전 및 크기 변환을 통하여 Style Transfer의 난이도를 향상시켜 학습을 일반화(Random Rotation [-15도 ~ 15도] & Random Flip 적용 [0.5의 확률])
    - **TPS[Thin Plate Splines] with Recognizer**
        - Recognizer : Text Image를 잘 읽게하기 위해 Pretrained Recognizer 도입
        - Swap Text 기법을 적용하여 Feature Extraction과 FC Layer를 통해 텍스트 윤곽을 파악할 수 있는 Anchor Point를 얻어 텍스트의 방향에 대한 정보를 제공하는 모듈
        - 부분적으로 속성을 분리하여 학습의 난이도를 낮추고, Text Style의 올바른 정보를 전송
- **Gradient Block**
    - 데이터셋에 존재하지 않는 패턴의 스타일에 대해서 변환되지 않고 출력될 가능성을 방지하기 위한 전략
- **Only in Reference**
    - BRM 모듈의 출력 이미지인 Inpainting Image와 Font Style이 Transfer된 Text를 Fusion하는 것이 아닌, 단순히 Inpainting Image를 참고하여 배경을 제거하면서 스타일이 적용된 Text를 Fusion하는 전략
- Label이 지정된 합성 데이터셋과 준지도 학습 방식을 위해 Label이 지정되지 않은 현실 데이터셋으로 훈련
---
**MOSTEL 데이터셋**

**[합성 이미지 데이터]** : 기존의 MOSTEL 모델은 이미지 내에 있는 영어 글자 스타일을 다른 영어 단어에 반영한 이미지를 생성하는 모델이다. 본 프로젝트는 영어가 아닌 한국어를 영어로 바꾸어 이미지를 생성하는 모델이므로, 영어로만 학습된 MOSTEL을 Fine Tuning하기 위해 한국어-영어 버전의 데이터셋 생성하였다.
<img width="866" alt="스크린샷 2023-07-09 오후 5 30 56" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/0aff6561-98f5-462a-bfc5-8a7296c9e679

**[합성 이미지 데이터 : Word & Sentence]**

- 원래 MOSTEL의 데이터셋은 단어 단위(word-level)의 텍스트 이미지 데이터셋으로만 구성되어 있지만, 아래 이미지와 같이 실제 간판이나 영상 내 글자는 띄어쓰기가 존재하거나 두 단어 이상의 영어로 이루어져 있다.
- 이를 고려하여 띄어쓰기가 있는 한국어와 영어 말뭉치 각각 15만 개와 띄어쓰기가 없는 한국어와 영어 말뭉치 각각 10만 개로 데이터를 생성하였다.
<img width="500" alt="스크린샷 2023-07-09 오후 5 31 17" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/a4b29c9d-1a9a-480f-aed2-a77626265612">

**[Custom 합성 이미지 데이터 : 기존 Background]**
<img width="500" alt="스크린샷 2023-07-09 오후 5 31 29" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/7bb31813-6f66-43d7-9f56-69332f6ae0ed">


- 기존 데이터셋 : 위의 사진과 같이 현실에서는 글자 배경이 단순하지만, 기존에 생성한 데이터셋은 현실에서 보기 힘든 복잡한 배경을 사용하여 데이터셋을 생성하였다.
- 기존 데이터셋으로 학습시킨 결과, 배경 이미지가 현실과 차이나는 Domain Gap이 커지는 문제로 Inference 성능 결과가 좋지 않았다.

<img width="867" alt="스크린샷 2023-07-09 오후 5 32 06" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/47c5b57f-f384-43df-a871-03bc158aee71">


→ 이를 해결하기 위해 복잡한 배경을 제거하고, 단색 배경을 추가하여 새로운 데이터셋을 생성하였다.

**[Custom 합성 이미지 데이터 : 재생성 Background]**

- 재생성한 데이터셋 : 학습에 방해가 되는 복잡한 배경 이미지를 제거하고, 단조로운 사진 배경 이미지 8,000장과 단색 배경 8,000장을 추가하여 새로운 데이터 셋을 생성하였다.
- 재생성한 데이터셋으로 학습시킨 결과, 현실과 차이나는 Domain Gap의 문제를 해결할 수 있었으며, 이에 따라 아래의 Inference 이미지를 통해 Background와 Text를 잘 분리하여 Inpainting하는 것을 볼 수 있다.

<img width="867" alt="스크린샷 2023-07-09 오후 5 32 32" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/ebc4d52c-1c1f-4586-9186-9d37af79ad5a">

**[Custom 합성 이미지 데이터 : Font Style]**
<img width="863" alt="스크린샷 2023-07-09 오후 5 32 52" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/12340e33-6372-4862-ad67-2dbeba9d29f2">


- 기존 데이터셋의 Font Style은 일정한 폰트와 크기, 각도, 색으로 생성하였으며, 이에 따라 한정된 Font Style에 과적합되어 Target Text에 Font Style을 적용시킬 수 없었다.
- 이를 해결하기 위해 상업, 광고, 포스터에 자주 사용되는 108개의 다양한 폰트와 크기, 각도, 색을 다르게 하여 생성한 결과, 위의 사진과 같이 Font Style을 제대로 적용시키는 것을 볼 수 있다.

**[Custom 현실 이미지 데이터]**

- Label이 지정되지 않은 현실 이미지 데이터셋을 통해 Semi-Supervised Learning이 가능
- Target Text에 Font Style을 입힌 최종 이미지의 Label을 원본 이미지로 줌으로써 Background에서 Text가 지워진 Inpainting Image와 마스킹된 이미지가 없는 실제 이미지만으로도 학습을 가능하게 하여 Domain Gap을 줄였다.
<img width="422" alt="스크린샷 2023-07-09 오후 5 33 43" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/0db3eeb0-0d43-4f73-a5e4-88a1c18344f2">
    
- 영어 현실 이미지 데이터는 MOSTEL Github에 제공되어 있는 데이터셋을 사용하였으며, 한국어 현실 이미지 데이터는 AI HUB에 제공되어 있는 “야외 실제 촬영 한글 이미지” 데이터셋 책 표지 800장을 사용하여 데이터셋을 생성하였다.

<img width="861" alt="스크린샷 2023-07-09 오후 5 34 02" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/9a84314a-6f0d-4ebe-9885-92ec581292f6">

**[최종 MOSTEL 훈련 데이터셋]**

<img width="1073" alt="스크린샷 2023-07-09 오후 5 35 17" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/0191ba7d-8a7c-49b6-a1cb-e8fce33602c9">


- 합성 이미지와 현실 이미지를 7:1 Batch의 비율로 하여 정성적으로 Text Style Transfer 결과를 확인하면서 평가하고, 이에 더하여 정량적으로 Loss의 모니터링, Metrics를 통해 Learning Rate를 0.00005로 15만 EPOCH 학습하고, 이후에 Learning Rate를 0.00004로 감소시켜 7만 EPOCH을 학습하여 총 22만 EPOCH을 146시간 학습하였다.

**[MOSTEL 개선 전 후 비교]**

<img width="1052" alt="스크린샷 2023-07-09 오후 5 37 03" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/0be2a1e8-d378-47d8-a7cc-1d3c7a5c38d7">

[COMPARISION MODEL : **MOSTEL** vs. **SRNet**]

- SRNet은 합성 이미지로만 학습이 가능하여 배경의 텍스처 보존이 어렵고, 동시에 작업이 이루어지다 보니 Bias가 발생하여 실제 영상에서 성능이 저하되는 문제가 발생하였다.
<img width="1032" alt="스크린샷 2023-07-09 오후 5 37 28" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/cf79dead-198b-402a-8945-4d288bd52cee">

- SRNet은 MOSTEL과 다르게 단순히 Text Style을 추출함과 동시에 Text를 제거한 Background를 추출하여 두 결과값을 Fusion한다. 편집 과정에서 이미지 전체 픽셀을 고려하여 배경과 글자 영역을 잘 분리하지 못 하고, 픽셀의 배경 영역에 변화를 일으키는 문제가 발생되었다.
    
<img width="1035" alt="스크린샷 2023-07-09 오후 5 37 58" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/8481ec7d-36b3-45ce-aad1-22b58c4f7592">

    
- 반면에 MOSTEL은 배경과 글자를 따로 분리하여 학습하는 구조로, 바뀌어야 할 픽셀의 위치를 Masking하여 Guide함으로써 글자에 변환을 적용할 때 배경은 영향을 받지 않는다.
<img width="1027" alt="스크린샷 2023-07-09 오후 5 38 33" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/00b52188-21c6-483c-998a-05bd6dcff2f7">


- **Text Inpainting 결과**
<img width="1029" alt="스크린샷 2023-07-09 오후 5 38 52" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/ded29a85-d706-4e68-a6d7-78313f9edbcd">

    - SRNet에 비해 MOSTEL은 배경 영역을 최대한 보존하여 Text를 Inpaint하는 것을 볼 수 있다.
 

- **Style Transfer 결과**
<img width="1034" alt="스크린샷 2023-07-09 오후 5 39 16" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/85a23c9d-3204-4c6c-80f3-dd8ef3961436">

---
**[MOSTEL Loss]**

- MOSTEL은 각각의 이미지에 대해 GAN Loss, L2 Loss, Dice Loss, Perceptual Loss, Style Loss, VGG Loss, Recognizer Loss를 채택하여 손실을 계산한다.
- 모델은 학습을 진행하면서 Background Inpainting Image, 원본 이미지의 Masking Image, 타겟 이미지의 Masking Image, 최종적으로 원본 이미지의 텍스트 스타일을 타겟 텍스트에 적용시킨 Fusion mage를 생성한다.
- Editing Guidance의 Image인 두 개의 Masking Image는 정답 이미지 텐서와 생성된 이미지 텐서 간의 교집합을 계산하여 평균을 구하고 음수를 취하는 Dice Loss로 최적화한다.
- **Background Inpainting Image**는 생성된 이미지 텐서의 로그값 평균을 계산하고 음수를 취하여 Loss를 계산하는 GAN Loss와 정답 이미지 텐서와 생성된 이미지 텐서 간 차이의 제곱을 계산하여 평균을 구하는 L2 Loss, Dice Loss로 최적화하여 생성된다.
- **Fusion Image**에는 MSE 평균 제곱의 오차를 계산하는 VGG Loss가 채택되는데, VGG Loss는 사실적인 이미지 생성을 위한 Perceptual Loss와 수준 높은 폰트 스타일 적용을 위한 Style Loss를 반영한다. Perceptual Loss와 Style Loss는 정답 이미지 텐서와 생성된 이미지 텐서 사이의 절댓값 차이를 계산하여 계산된 차이의 평균을 구하는 L1 Loss를 채택한다. 또한, 글자 인식을 위한 Recognizer Loss는 정답 이미지 텐서와 생성된 이미지 텐서의 로그 확률을 계산하여 음수를 취한 후 평균을 계산하는 Cross Entropy Loss를 채택한다. 최종적으로 Fusion Image는 GAN Loss와 VGG Loss, L2 Loss, Dice Loss, Recognizer Loss로 최적화하여 생성된다.

<img width="1061" alt="스크린샷 2023-07-09 오후 5 45 15" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/d6e63cb3-1611-4233-8549-c861362cbd80">

- Discriminator Fusion Loss와 Discriminator Background Inpaint Loss는 정답 이미지 텐서와 생성된 이미지 텐서 간의 차이를 측정하는 Binary Cross Entropy Loss에 음수를 취하여 계산된다.
- 모델 성능 개선 전략 적용 전의 Fusion Loss와 Background Inpaint Loss는 점차 하락하긴 하지만 심각하게 불안정한 경향을 나타낸다. 성능 개선 전략을 적용한 후의 Fusion Loss는 미세하게 튀는 경향을 보이지만 적용 전의 Loss에 비해 눈에 띄게 안정적으로 감소한다. 또한, Background Inpaint Loss는 적용 전과 비교했을 때 안정적으로 1.38으로 수렴하는 것을 볼 수 있다.

**[MOSTEL METRICS]**

<img width="1296" alt="스크린샷 2023-07-09 오후 5 45 47" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/bac32d5d-1ec3-49e6-9067-9d64eb9f20f6">

- **PSNR**[Peak Signal to Noise Ratio] : 원본 이미지와 생성된 이미지 간의 평균 제곱 오차를 측정하여 로그 스케일로 변환한 값으로, 이미지의 최대 신호와 잡음의 비율을 측정하는 지표이다. 원본과 생성된 이미지 간의 차이가 적을수록 값이 높아지므로, 증가하는 방향으로 학습되어야 한다.
- **SSIM**[Structural Similarity Index] : 인간의 시각 시스템이 이미지의 품질을 인식하는 방식을 모델링한 것으로, 원본 이미지와 생성된 이미지 간의 밝기, 대비, 품질의 구조적 유사성을 측정하는 지표이다. 값이 1에 가까울수록 두 이미지의 구조적 유사성이 높다는 것으로, 증가하는 방향으로 학습되어야 한다.
- **MSE**[Mean Squared Error] : 원본 이미지와 생성된 이미지 간의 차이를 제곱하여 평균을 계산하는 측정 지표로서, 두 이미지의 유사성을 비교하는데 사용된다. 유사할 수록 값이 작아지므로, 감소하는 방향으로 학습되어야 한다.
- **FID**[Frechet Inception Distance] : 원본 이미지와 생성된 이미지의 특징을 추출한 후에 평균과 공분산을 계산하여 두 이미지 간의 차이를 계산하는 지표이다. 두 이미지 간의 차이가 적을수록 값이 작아지므로, 감소하는 방향으로 학습되어야 한다.
- 모델 성능 개선 전략을 적용하여 학습시킨 결과, 위 그래프와 같이 PSNR과 SSIM은 증가하는 방향으로 학습되었으며, MSE와 FID는 하락하는 방향으로 학습되었다.
- 평균적으로 학습이 잘 되었다고 판단한 Iteration은 **PSNR : 24.6147, SSIM : 0.8186, MSE : 0.0049, FID : 40.9786의 값을 가지는 21만 번**으로 선정하였다.

---

## AI를 활용한 영상 내 텍스트 자동 번역 및 편집 기능을 통한 Projection Method

<img width="1056" alt="스크린샷 2023-07-09 오후 5 46 28" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/c4c0c5df-cf3f-492a-ad6f-d381b11daf50">

1. 프레임 선택
2. OCR을 통하여 글자가 있는 좌표를 찾고, 글자를 인식
3. 좌표를 통해 이미지를 자른 후 한영 번역
4. 번역된 글자에  Font Style Transfer
5. 원래 글자 위치에 Projection

**[Frame To Video]**

<img width="545" alt="스크린샷 2023-07-09 오후 5 46 52" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/a4630754-3911-4ea7-9f13-45ca4926d9bb">

- Text Font Style Transfer를 적용한 프레임 단위를 영상(1초에 약 60 프레임)으로 합하여 사용자가 다운로드 할 수 있는 영상을 생성한다.

## AI를 활용한 영상 내 텍스트 수동 번역 및 편집 기능

<img width="1190" alt="스크린샷 2023-07-09 오후 5 47 57" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/150f5c73-6f3d-4e41-a3d4-b8fd19c80782">

1. 편집된 영상의 프레임을 선택하여 원본 영상의 프레임으로 복원
2. 번역 및 편집을 적용할 글자의 좌표 클릭
3. 원하는 번역어 입력
4. 입력된 글자에 원본 글자 Font Style Transfer
5. 원래 글자 위치에 Projection

---

## AI를 활용한 영상 내 텍스트 제거 기능

<img width="792" alt="스크린샷 2023-07-09 오후 5 48 35" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/f33b9070-fa11-4b76-941a-849d7eda8de1">


1. 편집된 영상의 프레임을 선택하여 원본 영상의 프레임으로 복원
2. 글자를 제거할 좌표 클릭
3. 제거한 이미지를 원래 글자 위치에 Projection

[MOSTEL BRM 모듈 Custom화]

<img width="1275" alt="스크린샷 2023-07-09 오후 5 49 07" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/f6983787-13ac-47eb-a699-adf9048d06e1">

- **BRM의 Inpainting 원리** : Masking Image로 제거해야 하는 영역을 Guide하여 텍스트를 제거

<img width="1273" alt="스크린샷 2023-07-09 오후 5 49 30" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/7729f228-e30b-432b-8b9e-cf635927c78d">


- 기존 MOSTEL BRM 모듈의 Inpainting 원리로 학습하였을 때 글자 테두리가 남는 문제가 발생하였으며, 자연스러운 배경 이미지를 생성하기 위해 **cv2.Dilate**를 사용하여 **Masking Image에 글자 팽창을 적용**시켰다. 적용시킨 Masking Image를 Guide한 결과 Background를 보존한 채로 글자만 제거하여 성능을 개선하였다.

[MOSTEL Pre-Transformation 모듈 Custom화]

<img width="1275" alt="스크린샷 2023-07-09 오후 5 50 41" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/fad091a5-a2a8-4ba7-a7f6-80455dccad95">

- **TMM의 Text Recognition 원리** : 글자를 인식할 수 있는 Recognizer를 사용하여 글자의 위치, 방향, 색상 등 원본 이미지의 글자에 대한 특징을 Target Text에 적용
- 영어로만 학습되어 있기에 한국어 Font Style을 학습하지 못 하고 Target Text에 Font Style이 적용되지 않는 문제가 발생하였으며, 이를 해결하기 위해 Mostel의 구조 파악 후 Recognizer 모듈을 커스텀하여 **한국어와 영어 두 언어 모두 인식**할 수 있도록 학습하여 성능을 개선하였다.

---

## 향후 계획

### 신경망 기반 고화질 변환 : Real-ESRGAN

<img width="769" alt="스크린샷 2023-07-09 오후 5 51 06" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/93db93d6-a6d1-4892-be14-ca6c643b7f69">

- 기존 Text 이미지에 비해 저화질로 생성된 Text Font Style Transfer 이미지의 화질을 높이기 위해 GAN을 활용하여 현실적이고 자연스러운 이미지를 생성하여 시각적인 품질 향상시킨다.

### 객체 탐지 및 추적 : Siamese Network

<img width="1284" alt="스크린샷 2023-07-09 오후 5 51 29" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/5d604d45-1d7d-4b4d-b120-b66ed92fa7a5">

- 기존의 편집된 영상은 프레임 합성 시에 프레임 간의 차이가 존재하여 흔들림 또는 불일치 현상이 발생한다. 이를 개선하기 위해 Siamese Network를 사용하여 두 개의 프레임을 비교하여 프레임 합성 시에 발생하는 흔들림 현상을 최소화하고, 자연스러운 동영상 생성한다.

---

## 다양한 분야로의 확장성

### 타 분야 적용 1 : 포스터, 상품

<img width="968" alt="스크린샷 2023-07-09 오후 5 52 12" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/ebe4bd12-4026-4cda-ab7b-7e8d8668978f">

- 영화, 드라마 이외에도 원본 이미지의 Text Font Style을 학습하여 번역된 Text에 Font Style Transfer를 적용하여 포스터, 상품 등 다양하게 사용 가능하다.

### 타 분야 적용 2 : 번역기

<img width="1279" alt="스크린샷 2023-07-09 오후 5 52 39" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/845531fc-ac66-4588-b677-8902139159ec">


- 네이버에서 진행중인 “더 잘 읽히는 번역기” 프로젝트의 일부로, 현재 원본 이미지 내의 텍스트를 지우고 번역된 텍스트를 Fusion하는 프로젝트가 존재한다.

<img width="1276" alt="스크린샷 2023-07-09 오후 5 53 03" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/74752125-241e-4a3b-b9d7-66110735cc99">

- 위의 사진과 같이 파파고 번역기는 배경이 완전히 지워지지 않고 Font Style을 반영하지 못 하지만, 우리의 모델을 배경을 최대한 보존하여 글자 색상과 Font Style을 반영할 수 있다.

### 편집 비용 절감 가능

<img width="577" alt="스크린샷 2023-07-09 오후 5 53 39" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/9395a970-c6cf-4c10-8413-2fab9272871c">

- 현재 10초 길이 영상의 컴퓨터 그래픽 작업의 편집 비용은 10만 원부터 35만 원까지 수작업으로 진행되고 있으며, 작업일은 2일에서 5일이 소요된다.
- 컴퓨터 그래픽 작업 분야에서 AI를 활용한다면 시간적, 금전적 기회비용을 절감시킬 수 있으며, 더 나아가 증가하는 K 콘텐츠 산업의 수출에 있어서 해외 콘텐츠 접근성을 높이고, 국내 콘텐츠 수출 시장의 규모를 더욱 성장시킬 수 있다.

---

## 웹사이트 구상도

<img width="1287" alt="스크린샷 2023-07-09 오후 5 54 25" src="https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-Video/assets/121469490/17ae7f79-fa31-480b-a6df-1c9b7b6bfb32">

- 위에서 명시한 세 가지 기능을 추가한 웹사이트의 구상도로, 해당 웹사이트는 **회원가입 기능**과 **로그인 기능**, **편집 기록 기능**, **편집된 영상 재편집 기능**, **영상 업로드 기능**, **영상 저장 기능**, **글자 재생성 기능**, **글자 제거 기능**을 제공한다.

---

**참고 문헌**

Qu, Yadong, et al. "Exploring Stroke-Level Modifications for Scene Text Editing." arXiv preprint arXiv:2212.01982 (2022).

Liao, Minghui, et al. "Real-time scene text detection with differentiable binarization and adaptive scale fusion." IEEE Transactions on Pattern Analysis and Machine Intelligence 45.1 (2022): 919-931.

Wu, Liang, et al. "Editing text in the wild." Proceedings of the 27th ACM international conference on multimedia. 2019.

---

## Installation

### Requirements
~~~
git clone https://github.com/Yu-Miri/Text-Translation-and-Font-Style-Editing-in-video.git
conda create —name MOSTEL python=3.7.12 -c conda-forge
conda activate MOSTEL
pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 -f https://download.pytorch.org/whl/torch_stable.html
pip install mmcv-full==1.6.0 -f https://download.openmmlab.com/mmcv/dist/cu101/torch1.7/index.html
pip install -r requirements.txt
conda uninstall pytorch
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorchinput_d
~~~

---
### Training

- Mostel Train
~~~
python train.py —config configs/mostel-train.py
~~~

- Mostel Erase Train
~~~
python train_erase.py —config configs/erase-train.py
~~~

### Predict & Evaluation

- Predict
~~~
python predict.py --config configs/mostel-train.py --input_dir datasets_eval/i_s/ --save_dir results_eval --checkpoint checkpoint/train_step-210000.model --slm
~~~

- Evaluation : PSNR, SSIM, MSE, FID
~~~
python evaluation.py --gt_path datasets_eval/t_f/ --target_path results_eval
~~~
