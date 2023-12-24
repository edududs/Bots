import os
import sys
from pathlib import Path

import moviepy.editor as mpe
from pytube import Search, YouTube

from commands.libs.utils import is_valid_url

BASE_ROOT = Path(os.path.dirname(os.path.abspath(sys.argv[0])))


class AudioEditor:
    BASE_ROOT = os.path.dirname(os.path.abspath(sys.argv[0]))

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.file_path = str(Path(self.BASE_ROOT, file_name))
        self.audio_file_editor = mpe.AudioFileClip(self.file_path)

    def convert_audio(self, file: str | None = None):
        if file is not None:
            output_file = str(Path(self.BASE_ROOT, file))
        else:
            output_file = str(Path(self.BASE_ROOT, self.file_name))
        self.audio_file_editor.write_audiofile(output_file, codec="libmp3lame")
        return output_file


class YoutubeDownloader:
    def __init__(self):
        self.yt = None
        self.audio_file = ""
        self.audio_file_name = ""
        self.audio_file_name_mp3 = ""

    def download_audio(self, url: str, output_path: str = "", convert_to_mp3=False):
        if not is_valid_url(url):
            print("Defina primeiro o link do vídeo")
            return
        try:
            self.yt = YouTube(url)
            streams = self.yt.streams.filter(only_audio=True).first()
            if streams is not None:
                if not os.path.exists(output_path):
                    output_path = str(self.verify_download_directory())
                self.audio_file = streams.download(output_path)
                self.audio_file_name = str(Path(self.audio_file).name)
                print(f"O áudio do vídeo foi baixado em: {self.audio_file}")
                if convert_to_mp3:
                    print("Convertendo o video com apenas o áudio em .mp3")
                    self.audio_file = self._convert_video_to_mp3()
                return self.audio_file
        except Exception as e:
            raise e

    def verify_download_directory(self):
        download_path = BASE_ROOT / "downloads" / "audio"
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        return download_path

    def _convert_video_to_mp3(self):
        if self.audio_file_name.endswith(".mp4"):
            audio_file = AudioEditor(self.audio_file_name)
            self.audio_file_name_mp3 = self.audio_file_name.replace(".mp4", ".mp3")
            output_converted_audio = audio_file.convert_audio(self.audio_file_name_mp3)
            os.remove(self.audio_file)
            return output_converted_audio
        if self.audio_file_name != "":
            audio_file = AudioEditor(self.audio_file_name)
            output = audio_file.convert_audio()
            return output
        else:
            print("Defina o nome do arquivo de audio")


class YoutubeSearch:
    def __init__(self):
        self.result = None

    def search_one(self, input_text: str):
        search_results = []

        try:
            yt_search = Search(input_text)
            search_results = yt_search.results
            if search_results:
                result: YouTube = search_results[0]
                self.result = result
                print(f"Título do vídeo:{self.result.title}")
                return self.result
            print("Nenhum resultado encontrado")
            

        except Exception as e:
            print(f"Erro na pesquisa: {str(e)}")
            raise e

    def search_multiple(self, input_text: str):
        search_results = []
        videos = {}
        try:
            yt_search = Search(input_text)
            search_results = yt_search.results
            if search_results != [] and search_results is not None:
                for i, result in enumerate(search_results):
                    url = f"https://www.youtube.com/watch?v={result.video_id}"
                    video_info = {
                        f"Option{i}": {
                            "title": result.title,
                            "id": result.video_id,
                            "url": url,
                        }
                    }
                    videos.update(video_info)
                return videos

        except Exception as e:
            print(f"Erro na pesquisa: {str(e)}")
            raise e


if __name__ == "__main__":
    ...
