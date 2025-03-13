from openai import OpenAI
import streamlit as st
from io import BytesIO
from dotenv import load_dotenv
import os
import base64
from PIL import Image

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = api_key)

def ai_describe(image_url):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "이 이미지에 대해서 자세하게 설명해 주세요."},
            {"type": "image_url",
                "image_url": {"url": image_url,},
            },
        ],
        }
    ],
    max_tokens=1024,
    )
    result = response.choices[0].message.content
    print("결과 >> ", result)
    return result

def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def ai_describe_2(image):
    try:
        base64_image = encode_image(image)
        
        response = client.chat.completions.create(
            model="gpt-4o",

            
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이 이미지에 대해서 자세하게 설명해 주세요."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류 발생: {str(e)}"

st.title("AI 도슨트: 이미지를 설명해드려요!")
tab1, tab2 = st.tabs(["이미지 파일 업로드", "이미지 URL 입력"])

with tab1:
    uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, width=300)
        if st.button("해설", key="unique_key_1"):
            image = Image.open(uploaded_file)
            result = ai_describe_2(image)
            st.success(result)

with tab2:
    input_url = st.text_area("여기에 이미지 주소를 입력하세요", height=70)
    if st.button("설명", key="unique_key_2"):
        if input_url:
            try:
                st.image(input_url, width=300)
                result = ai_describe(input_url)
                st.success(result)
            except:
                st.error("요청 오류가 발생했습니다!")
        else:
            st.warning("텍스트를 입력하세요!")