from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path

from PIL import Image

from commands.libs.utils import get_existent_file_path, is_img


class Conversor(ABC):
    @abstractmethod
    def convert(self, file_path: str | Path, target_format: str = "") -> None:
        """Common conversion logic for all converters."""


class BaseConverter(Conversor):
    def rename_file(self, file_path: str | Path, new_name: str) -> Path:
        """
        Renomeia a imagem com um novo nome baseado no contador.

        Parameters:
            image_path (str): O caminho para a imagem.

        Returns:
            str: O novo caminho para a imagem renomeada.
        """

        # Obtém o diretório e o nome do arquivo sem extensão
        file_path = get_existent_file_path(file_path)
        extension = file_path.suffix
        new_name = f"{new_name}{extension}"
        new_file_path = Path(file_path.parent, new_name)

        # Remove o novo arquivo se ele já existir
        if new_file_path.exists():
            os.remove(new_file_path)

        # Renomeia a imagem
        os.rename(file_path, new_file_path)

        return new_file_path

    def process_path(self, directory: str | Path) -> None:
        # Transforma o diretório em um Path
        directory = Path(directory).resolve()

        # Verifica se o diretório é um arquivo
        if directory.is_file():
            self.convert(directory)
            return

        # Percorre todos os arquivos no diretório
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)

            # Verifica se é um arquivo e se é uma imagem
            if is_img(file_path):
                self.convert(file_path)


class ConversorManager(ABC):
    @abstractmethod
    def menu(self) -> None:
        """Display the conversion options."""

    @abstractmethod
    def convert(self, caminho_imagem: str, target_format: str) -> None:
        """Convert the image to the specified format."""


class BaseIMGConverter(BaseConverter):
    def __init__(self, target_format="") -> None:
        super().__init__()
        self._target_format = target_format.upper()
        self._supported_extensions = self.get_supported_extensions()

    def get_supported_extensions(self) -> set:
        """
        Obtém as extensões suportadas pelo Pillow.

        Returns:
            set: Um conjunto de extensões suportadas.
        """
        return set(Image.registered_extensions())

    def convert(self, file_path: str | Path, target_format=None) -> None:
        """
        Common conversion logic for all converters.

        Parameters:
            file_path (str): The path to the input file.
            target_format (str): The target format for conversion. If not provided,
                                the format is determined based on the file extension.

        Raises:
            FileNotFoundError: If the input file does not exist.
            ValueError: If the target format is not supported.
        """

        file_path = get_existent_file_path(file_path)
        directory, file_name = file_path.parent, file_path.stem
        extensao = file_path.suffix

        # Se o formato alvo não for fornecido, tenta determinar automaticamente com base na extensão
        target_format = (
            target_format.upper().replace("-", "")
            if target_format
            else extensao[1:].upper()
        )

        # Verifica se o formato alvo é suportado
        # if target_format not in self._supported_extensions:
        #     raise ValueError(f"Unsupported target format: {target_format}")

        # Cria o novo caminho com a extensão correta
        novo_caminho = os.path.join(directory, f"{file_name}.{target_format.lower()}")

        # Abre a imagem e a salva no formato alvo
        with Image.open(file_path) as img:
            img.save(novo_caminho, format=target_format)

        # Opcional: Remove o arquivo original
        os.remove(file_path)

        print(f"Imagem convertida: {file_path} -> {novo_caminho}")


class BaseVideoConverter(BaseConverter):
    def convert(self, file_path: str | Path, target_format: str = "") -> None:
        ...
