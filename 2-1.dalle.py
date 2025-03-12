import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
from PIL import Image
import base64
import io

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 실제 이미지 값을 json값으로 리턴 받음.
def get_image(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        response_format='b64_json',
        n=1       
    )

    response = response.data[0].b64_json # DALLE로부터 Base64 형태의 이미지를 얻음.
    image_data = base64.b64decode(response) # Base64로 쓰여진 데이터를 이미지 형태로 변환
    image = Image.open(io.BytesIO(image_data)) # '파일처럼' 만들어진 이미지 데이터를 컴퓨터에서 볼 수 있도록 Open
    return image


st.title("그림 그리는 AI 화가 서비스 🧑‍‍🎨")
st.image("images/robot_painter.jpg", width=300)
st.write("🎨 Tell me the picture you want. I'll draw it for you!")

prompt = st.text_area("원하는 이미지의 설명을 영어로 적어보세요.", height=200)

if st.button("Painting"):
    if prompt.strip():
        try:
            image = get_image(prompt)
            st.image(image, width=300)
        
        except Exception as e:
            st.error(f"이미지 생성 중 오류 발생: {e}")
    else:
        st.warning("이미지 설명을 입력해주세요!")
