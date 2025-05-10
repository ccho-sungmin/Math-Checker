
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI API Key (환경변수에서 불러오기 권장)
openai.api_key = os.environ.get("OPENAI_API_KEY", "sk-your-key-here")

@app.route("/verify", methods=["POST"])
def verify():
    try:
        input_text = request.json.get("text", "").strip()
        if not input_text:
            return jsonify({"error": "입력된 텍스트가 없습니다."}), 400

        messages = [
            {"role": "system", "content": "너는 수학 문제 조건을 분석하여, 해당 조건을 만족하는 함수가 존재하는지 판단하고 예시를 제공하는 수학 전문가야."},
            {"role": "user", "content": input_text}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2
        )

        result = response.choices[0].message.content
        return jsonify({"result": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
