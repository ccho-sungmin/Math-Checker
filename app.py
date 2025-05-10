
import streamlit as st
import requests
import json

st.set_page_config(page_title="수학 함수 조건 검증기", page_icon="🧠")
st.title("🧠 수학 함수 조건 검증기")

st.markdown("자연어 또는 수식 조건을 입력하세요. GPT-4가 조건을 해석하고 함수 존재 여부를 판별합니다.")

# 사용자 입력 받기
user_input = st.text_area("✍️ 수학 조건을 입력하세요", height=150, placeholder="예: f(x+pi) = f(x) + c")

if st.button("검증하기"):
    if not user_input.strip():
        st.warning("조건을 입력해주세요.")
    else:
        with st.spinner("GPT-4가 분석 중..."):
            try:
                headers = {
                    "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
                    "Content-Type": "application/json"
                }

                data = {
                    "model": "gpt-4",
                    "messages": [
                        {"role": "system", "content": "너는 수학 문제 조건을 분석하여, 해당 조건을 만족하는 함수가 존재하는지 판단하고 예시를 제공하는 수학 전문가야."},
                        {"role": "user", "content": user_input.strip()}
                    ],
                    "temperature": 0.2
                }

                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(data, ensure_ascii=False)
                )

                if response.status_code == 200:
                    result = response.json()["choices"][0]["message"]["content"]
                    st.success("검증 완료!")
                    st.markdown("**결과:**\n" + result, unsafe_allow_html=True)
                else:
                    st.error(f"오류 발생: {response.status_code}\n{response.text}")

            except Exception as e:
                st.error(f"예외 발생: {e}")
