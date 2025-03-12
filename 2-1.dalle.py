import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
from PIL import Image
from io import BytesIO

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 이미지 url을 받음
def get_image(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1       
    )
    image_url = response.data[0].url
    return image_url



st.title("그림 그리는 AI 화가 서비스 🧑‍‍🎨")
st.image("images/robot_painter.jpg", width=300)
st.write("🎨 Tell me the picture you want. I'll draw it for you!")

prompt = st.text_area("원하는 이미지의 설명을 영어로 적어보세요.", height=200)

if st.button("Painting"):
    if prompt.strip():
        try:
            image_url = get_image(prompt)
            st.image(image_url, width=300)
        
        except Exception as e:
            st.error(f"이미지 생성 중 오류 발생: {e}")
    else:
        st.warning("이미지 설명을 입력해주세요!")
