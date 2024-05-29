from agency_swarm.tools import BaseTool
from pydantic import Field
from pytube import YouTube
import openai
from dotenv import load_dotenv
import os

load_dotenv()

client = openai.Client()

class GetMP3(BaseTool):
    """This tool will get the mp3 file from the youtube video url """
    url: str = Field(
        ..., description="The URL of the youtube video"
    )

    def run(self):
        try:
            video = YouTube(self.url)
            stream = video.streams.filter(only_audio=True).first()
            stream.download(filename=f"{video.title}.mp3")
            print(f"The video, {video.title} is downloaded in MP3")
        except KeyError:
            print("Unable to fetch video information. Please check the video URL or your network connection.")

        return f"The video, {video.title} is downloaded in MP3 as {video.title}.mp3"

class AudioTranscriptionTool(BaseTool):
    """
    A tool for transcribing audio content using OpenAI's Whisper model. Efficient and accurate transcription of various audio formats into text.
    """

    audio_file_path: str = Field(
        ..., description="Path to the audio file to be transcribed"
    )

    def run(self):
        audio_file_path="./Doublë.mp3"
        audio_file= open(audio_file_path, "rb")
        response = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                    language="en",
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )       
        transcription_text = response.segments
        file_name = os.path.basename(audio_file_path)
        file_name_without_extension = os.path.splitext(file_name)[0]
        directory = "./Transcriptions"

        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, f"{file_name_without_extension}.txt")

        with open(file_path, "w") as file:
                file.writelines([str(item) + '\n' for item in transcription_text.items()])

        return "Transcription successful. The transcription text has been saved as the file: " + f"{file_name_without_extension}.txt in the directory, {directory}"

