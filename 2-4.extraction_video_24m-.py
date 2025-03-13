import streamlit as st
import os
import openai
from dotenv import load_dotenv
from moviepy import VideoFileClip
from pydub import AudioSegment

# video를 가져와 audio 추출하기
def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec='mp3')

# audio 크기 쪼개기
def split_audio(audio_path, chunk_size_mb=10):
    audio = AudioSegment.from_mp3(audio_path)
    chunk_size = chunk_size_mb * 1024 * 1024  # MB to Bytes
    chunks = []
    
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i+chunk_size]
        chunk_path = f"chunk_{i//chunk_size}.mp3"
        chunk.export(chunk_path, format="mp3", bitrate="32k")
        chunks.append(chunk_path)
    
    return chunks

# 쪼개진 audio에서 text를 추출하고 하나로 합치기
def transcribe_audio(audio_path, client):
    audio_chunks = split_audio(audio_path)  # Split into 10MB chunks
    full_transcription = ""

    for chunk in audio_chunks:
        with open(chunk, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        full_transcription += transcript.text + "\n"
        
        os.remove(chunk)  # Remove used chunk file
    
    return full_transcription

# 파일 저장하기
def save_file(content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    load_dotenv(override=True)
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    st.title("🎥 Video to Audio & Script Extractor")
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
    
    if uploaded_file is not None:
        temp_dir = "temp_files"
        os.makedirs(temp_dir, exist_ok=True)

        video_path = os.path.join(temp_dir, uploaded_file.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        audio_path = os.path.join(temp_dir, "extracted_audio.mp3")
        script_path = os.path.join(temp_dir, "transcribed_script.txt")

        st.info("Extracting audio...")
        extract_audio(video_path, audio_path)
        
        st.success("Audio extracted successfully! 🎵")
        
        st.info("Transcribing audio...")
        script_text = transcribe_audio(audio_path, client)
        save_file(script_text, script_path)
        
        st.success("Transcription completed! 📝")
        
        st.audio(audio_path, format='audio/mp3')
        
        st.subheader("Transcribed Script")
        st.text_area("", script_text, height=300)
        
        st.download_button("Download Audio", audio_path, file_name="extracted_audio.mp3")
        st.download_button("Download Script", script_path, file_name="transcribed_script.txt")
        
if __name__ == "__main__":
    main()