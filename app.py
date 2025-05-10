
import streamlit as st
import openai
from PIL import Image
import io
import base64

st.set_page_config(page_title="수학 함수 조건 검증기", page_icon="🧠")

st.title("🧠 수학 함수 조건 검증기")
st.markdown("자연어 또는 수식 조건을 입력하거나, 문제 이미지를 업로드하세요. GPT-4가 조건을 해석하고 함수 존재 여부를 판별합니다.")

# OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ASCII-safe 변환 함수
def remove_non_ascii(text):
    return ''.join(c for c in text if ord(c) < 128)

# 텍스트 입력
user_input = st.text_area("✍️ 수학 조건을 입력하세요", height=150, placeholder="예: f(x+y)=f(x)+f(y), f는 연속 아님, R → R")

# 이미지 업로드
uploaded_file = st.file_uploader("🖼️ 문제 이미지 업로드 (선택)", type=["png", "jpg", "jpeg"])

# 이미지 처리
image_data_url = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 이미지", use_column_width=True)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    image_data_url = f"data:image/png;base64,{img_b64}"

if st.button("검증하기"):
    if not user_input.strip() and not image_data_url:
        st.warning("텍스트 또는 이미지를 입력해주세요.")
    else:
        with st.spinner("GPT-4가 분석 중..."):
            try:
                messages = [{"role": "system", "content": "너는 수학 문제 조건을 분석하여, 해당 조건을 만족하는 함수가 존재하는지 판단하고 예시를 제공하는 수학 전문가야."}]

                if image_data_url and user_input.strip():
                    text = remove_non_ascii(user_input.strip())
                    messages.append({
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": image_data_url}},
                            {"type": "text", "text": f"조건: {text}"}
                        ]
                    })
                elif image_data_url:
                    messages.append({
                        "role": "user",
                        "content": [{"type": "image_url", "image_url": {"url": image_data_url}}]
                    })
                else:
                    text = remove_non_ascii(user_input.strip())
                    messages.append({"role": "user", "content": f"조건: {text}"})

                response = openai.chat.completions.create(
                    model="gpt-4-vision-preview" if image_data_url else "gpt-4",
                    messages=messages,
                    temperature=0.2
                )

                result = response.choices[0].message.content
                st.success("검증 완료!")
                st.markdown(f"**결과:**\n{result}", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"오류 발생: {e}")
