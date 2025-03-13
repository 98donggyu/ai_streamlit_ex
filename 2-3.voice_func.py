import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = api_key)

def text_to_voice(user_prompt, selected_option):
    audio_response = client.audio.speech.create(
            model="tts-1",
            voice=selected_option,
            input=user_prompt,
    )
    return audio_response

def save_audio(audio_response):
    audio_content = audio_response.content
    with open("temp_audio.mp3", "wb") as audio_file:
        audio_file.write(audio_content)
    return "temp_audio.mp3"

def main():
    st.title("OpenAI's Text-to-Audio Response")
    st.image("https://wikidocs.net/images/page/215361/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%EC%84%B1%EC%9A%B0.jpg", width=200)
    options = ['alloy', 'ash', 'coral', 'echo', 'fable', 'onyx', 'nova', 'sage', 'shimmer']
    selected_option = st.selectbox("성우를 선택하세요:", options)
    default_text = '오늘은 생활의 꿀팁을 알아보겠습니다.'
    user_prompt = st.text_area("인공지능 성우가 읽을 스크립트를 입력해주세요.", value=default_text, height=200)

    if st.button("Generate Audio"):
        st.audio(save_audio(text_to_voice(user_prompt, selected_option)), format="audio/mp3")

if __name__ == "__main__":
    main()