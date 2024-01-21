# Import necessary libraries
from pytube import YouTube
from moviepy.editor import VideoFileClip
import pytesseract
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import cv2
import os
process_path="C:\\work\\"

t="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Function to download YouTube video using pytube
def download_youtube_video(url, output_path=process_path+'downloaded_video.mp4'):
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video.download(output_path=output_path)
    
    output_path=output_path+'\\'+video.default_filename
    return output_path

# Function to extract frames from the downloaded video using MoviePy
def extract_frames(video_path, interval=1):
    clip = VideoFileClip(video_path)
    frame_paths = []
    for t in range(0, int(clip.duration), interval):
        frame_path = process_path+f"frames\\frame_{t}.jpg"
        clip.save_frame(frame_path, t)
        frame_paths.append(frame_path)
    return frame_paths

# Function to extract text from frames using pytesseract
def extract_text_from_frames(frames):
    extracted_text = ""
    for frame_path in frames:
        img = cv2.imread(frame_path)
        text = pytesseract.image_to_string(img, lang='gre')  # Use 'gre' for Greek language
        extracted_text += text + "\n"
    return extracted_text

def extract_audio(video_path, audio_path='extracted_audio.wav'):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(process_path+audio_path)
    return process_path+audio_path

def speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='el-GR')
        except sr.UnknownValueError:
            text = "Speech Recognition could not understand audio"
        except sr.RequestError as e:
            text = f"Could not request results from Google Speech Recognition service; {e}"

        return text

def main(url):
    video_path = download_youtube_video(url)
    audio_path = extract_audio(video_path)
    speech_text = speech_to_text(audio_path)
    #frames = extract_frames(video_path)
    #ocr_text = extract_text_from_frames(frames)
    #combined_text = ocr_text + "\n\nSpeech Text:\n" + speech_text
    combined_text = speech_text
    with open(process_path+"combined_extracted_text.txt", "w", encoding="utf-8") as file:
        file.write(combined_text)


if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=eOAVCynERjA"
    main(youtube_url)
