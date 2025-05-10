
import streamlit as st
import openai
from PIL import Image
import io

st.set_page_config(page_title="수학 함수 조건 검증기", page_icon="🧠")

st.title("🧠 수학 함수 조건 검증기")
st.markdown("자연어 또는 수식 조건을 입력하거나, 문제 이미지를 업로드하세요. GPT-4가 조건을 해석하고 함수 존재 여부를 판별합니다.")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Text input
user_input = st.text_area("✍️ 수학 조건을 입력하세요", height=150, placeholder="예: f(x+y)=f(x)+f(y), f는 연속 아님, ℝ → ℝ")

# Image upload
uploaded_file = st.file_uploader("🖼️ 문제 이미지 업로드 (선택)", type=["png", "jpg", "jpeg"])

# Convert image to base64 if uploaded
image_content = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 이미지", use_column_width=True)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    image_content = buf.getvalue()

# Combine both for GPT input
if st.button("검증하기"):
    if not user_input.strip() and not image_content:
        st.warning("텍스트 또는 이미지를 입력해주세요.")
    else:
        with st.spinner("GPT-4가 분석 중..."):
            try:
                messages = [
                    {"role": "system", "content": "너는 수학 문제 조건을 분석해서, 그 조건을 만족하는 함수가 존재하는지 판단하고 예시 함수도 가능한 경우 제공하는 전문가야."},
                ]
                if user_input.strip():
                    messages.append({"role": "user", "content": f"조건: {user_input.strip()}"})
                if image_content:
                    messages.append({
                        "role": "user",
                        "content": [{"type": "image_url", "image_url": {"url": "data:image/png;base64," + image_content.encode("base64").decode()}}]
                    })

                response = openai.ChatCompletion.create(
                    model="gpt-4-vision-preview" if image_content else "gpt-4",
                    messages=messages,
                    temperature=0.2
                )
                result = response.choices[0].message.content
                st.success("검증 완료!")
                st.markdown("**결과:**\n" + result)

            except Exception as e:
                st.error(f"오류 발생: {e}")
