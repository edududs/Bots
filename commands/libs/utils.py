import os
import re
from pathlib import Path
from urllib.parse import urlparse

NUM_OR_DOT_REGEX = re.compile(r"^[0-9.]$")
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


def get_existent_file_path(file_path: str | Path) -> Path:
    file_path = Path(file_path).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist")
    if not file_path.is_file():
        raise ValueError(f"{file_path} is not a file")
    return file_path


def is_img(file):
    extensoes_suportadas = [".jpg", ".jpeg", ".bmp", ".webp", ".png"]

    # Verifica se o path é um arquivo
    if os.path.isfile(file):
        # Obtém a extensão do arquivo
        _, extensao = os.path.splitext(file)

        # Verifica se a extensão está na lista de extensões suportadas
        if extensao.lower() in extensoes_suportadas:
            return True

    return False


def is_valid_url(input_string):
    try:
        result = urlparse(input_string)
        return all(
            [result.scheme, result.netloc]
        )  # Verifica se há esquema e local de rede
    except ValueError:
        return False


def is_num_or_dot(string: str) -> bool:
    """
    Check if a string contains only digits or a dot.
    Args:
        string (str): The input string to be checked.
    Returns:
        bool: True if the string contains only digits or a dot, False
        otherwise.
    """
    return bool(NUM_OR_DOT_REGEX.search(string))


def is_valid_number(string: str) -> bool:
    valid = False
    try:
        float(string)
        valid = True
        return valid
    except ValueError:
        valid = False
        return valid


def convert_to_number(string: str):
    """
    Converts a string to a number.

    Args:
        string (str): The string to be converted to a number.

    Returns:
        int or float: The converted number. If the string represents an integer, it returns an int. Otherwise, it returns a float.
    """
    if not is_valid_number(string):
        return

    number = float(string)
    if number.is_integer():
        return int(number)
    return number


def is_empty(string: str) -> bool:
    """
    Check if a given string is empty.
    Args:
        string (str): The string to check.
    Returns:
        bool: True if the string is empty, False otherwise.
    """
    return len(string) == 0


def formmat_result(result):
    if isinstance(result, int) or result.is_integer():
        return int(result)
    else:
        return round(result, 2)
