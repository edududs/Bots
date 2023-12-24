import os
import shutil
import tempfile
from typing import List

from moviepy.editor import VideoFileClip

from commands.libs.package_convert.models import (
    BaseIMGConverter,
    Conversor,
    ConversorManager,
)


class ImagemConversorManager(ConversorManager):
    def __init__(self, converters: List[BaseIMGConverter]) -> None:
        self.converters = converters

    def menu(self) -> None:
        print("Selecione uma das opções:")
        print("1. Converter para PNG")

    def convert(self, caminho_imagem: str, target_format: str) -> None:
        for converter in self.converters:
            if target_format.upper() in converter.get_supported_extensions():
                converter.convert(caminho_imagem, target_format)
                return
        print(f"Formato alvo {target_format} não suportado.")


class PNGConverter(BaseIMGConverter):
    def convert(self, file_path, target_format="a "):
        target_format = "PNG"
        return super().convert(file_path, target_format)


class JPGConverter(BaseIMGConverter):
    def convert(self, file_path, target_format=""):
        target_format = "JPEG"
        return super().convert(file_path, target_format)


class MP4Converter:
    CODECS = (
        ("MP4", "libx264"),
        ("WEBM", "libvpx"),
        ("MOV", "mov"),
        ("MPEG-1", "mpeg1video"),
        ("MPEG-2", "mpeg2video"),
        ("MPG", "mpeg2video"),
        ("MPEGPS", "mpeg2video"),
        ("MPEG4", "mpeg4"),
        ("AVI", "msmpeg4"),
        ("WMV", "wmv2"),
        ("FLV", "flv"),
        ("3GPP", "h263p"),
    )

    def start_conversion(
        self, selected_format: str, input_path: str, output_path: str = ""
    ):
        """
        Convert a video file to the specified format and save it to the output path.

        This function takes an input video file, converts it to the specified video format
        using the chosen codec, and saves the converted video to the output path.

        Args:
            input_path (str): The path to the input video file.
            output_path (str): The path where the converted video will be saved.
            selected_format (str): The desired format for the converted video.

        Raises:
            Exception: If any error occurs during the conversion process.

        Returns:
            None
        """
        print(input_path)
        if not input_path:
            return
        try:
            temp_output = tempfile.NamedTemporaryFile(
                suffix=f".{selected_format.lower()}", delete=False
            )

            codec = self.convert(selected_format)
            video_clip = VideoFileClip(input_path)
            video_clip.write_videofile(temp_output.name, codec=codec)

            if not output_path:
                output_path = self.generate_output_path(input_path)

            shutil.copy(temp_output.name, output_path)

            print(f"Conversão concluída.\nSalvo em: {output_path}")
        except Exception as e:
            print(f"Erro: {e}")

    def convert(self, selected_format):
        """
        Convert the selected format to the corresponding codec.

        Parameters:
            selected_format (str): The format to be converted.

        Returns:
            str: The corresponding codec for the selected format.
        """
        for extension in self.CODECS:
            if selected_format == extension[0]:
                return extension[1]

    def generate_output_path(self, input_path):
        """
        Generate a new output path based on the input file's path.

        Parameters:
            input_path (str): The path to the input video file.

        Returns:
            str: The new output path.
        """
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_directory = os.path.dirname(input_path)
        output_name = f"{file_name}_converted.mp4"
        output_path = os.path.join(output_directory, output_name)
        return output_path


class MP3Converter:
    ...


class ConversorFactory:
    @staticmethod
    def criar_conversor(target_format: str) -> Conversor:
        if target_format == "-png":
            return PNGConverter()
        elif target_format == "-jpg":
            return JPGConverter()
        # Adicione mais lógica para outros formatos, se necessário
        else:
            raise ValueError(f"Formato alvo {target_format} não suportado.")
