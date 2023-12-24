from __future__ import annotations

import asyncio
import os
import subprocess
from abc import ABC, abstractmethod
from typing import List

from pytube import YouTube
from translate import Translator

from commands.libs.conversor import (
    MP4Converter,
    PNGConverter,
    ImagemConversorManager,
    ConversorFactory,
)
from commands.libs.utils import is_valid_url
from commands.libs.youtube_manager import AudioEditor, YoutubeDownloader, YoutubeSearch


class CommandManager:
    def __init__(self) -> None:
        self.commands: List[CommandInfo] = []
        self.initialize_commands()

    def initialize_commands(self) -> None:
        """
        Initializes the commands for the API.

        This function adds the desired commands during initialization. It sets up the commands using the `add_command` method of the API class.

        Parameters:
            None

        Returns:
            None
        """
        # Adicione os comandos desejados durante a inicialização
        self.add_command(["hello", "ola", "oi"], SaudacaoCommand())
        self.add_command(["task"], AsyncTaskCommand())
        self.add_command(
            ["translate", "traduzir", "traduz", "traduza", "t"], TranslateCommand()
        )
        self.add_command(["help"], HelpCommand(self.commands))
        self.add_command(["convert", "converter", "converta"], Converter())
        self.add_command(["calc", "calculadora", "calcula"], Calculator())
        self.add_command(
            ["download", "baixar", "baixar-musica"], DownloadMusicCommand()
        )
        self.add_command(
            ["search", "procurar", "procurar-musica", "pesquisar-musica"],
            SearchYoutubeMusic(),
        )

    def add_command(self, aliases: List[str], command: Command) -> None:
        """
        Add a new command to the list of commands.

        Args:
            aliases (List[str]): A list of aliases for the command.
            command (Command): The command to be added.

        Returns:
            None
        """
        command_info = CommandInfo(aliases, command)
        self.commands.append(command_info)

    async def process_command(self, user_input) -> None:
        """
        Process a user command.

        Args:
            user_input (str): The input provided by the user.

        Returns:
            None: This function does not return anything.
        """
        command_name, *args = user_input.split()

        if command_name.lower() == "quit":
            print("\nSaindo do bot. Até mais!")
            asyncio.get_event_loop().stop()
        else:
            await self.execute_command(command_name.lower(), args)

    async def execute_command(self, command_name: str, args: List[str]) -> None:
        """
        Asynchronously executes a command based on the given command name and arguments.

        Parameters:
            command_name (str): The name of the command to be executed.
            args (List[str]): The list of arguments to be passed to the command.

        Returns:
            None: This function does not return anything.
        """
        found_command = None

        for command_info in self.commands:
            if command_name in command_info.aliases:
                found_command = command_info
                break

        if found_command:
            await found_command.command.execute(args)
            print(f"\nComando {command_name} executado com sucesso!\n")
        else:
            print(f"\nComando desconhecido: {command_name}\n")


class Command(ABC):
    @abstractmethod
    async def execute(self, args: List[str]) -> None:
        pass


class CommandInfo:
    def __init__(self, aliases: List[str], command: Command) -> None:
        """
        Initialize the class with the provided aliases and command.

        Args:
            aliases (List[str]): A list of strings representing the aliases for the command.
            command (Command): An instance of the Command class representing the command.

        Returns:
            None
        """
        self.aliases: List[str] = aliases
        self.command = command

    def __str__(self) -> str:
        return f"{self.aliases}"


class SaudacaoCommand(Command):
    async def execute(self, args) -> None:
        print("Olá!\nTudo bem?\n")


class Calculator(Command):
    async def execute(self, args) -> None:
        calculator_path = r"C:\Windows\System32\calc.exe"
        subprocess.run([calculator_path], check=True)


class AsyncTaskCommand(Command):
    def __init__(self):
        self.is_running = False

    async def execute(self, args) -> None:
        if self.is_running:
            print("A tarefa está em execução. Aguarde a conclusão.\n")
            return
        print("Iniciando a tarefa assíncrona.")
        self.is_running = True
        await self.run_async_task(args)
        self.is_running = False

    async def run_async_task(self, args) -> None:
        # Simule uma tarefa assíncrona aqui
        await asyncio.sleep(5)
        print(f"\nTarefa assíncrona concluída com argumentos: {args}")


class TranslateCommand(Command):
    async def execute(self, args: List[str]) -> None:
        if not args:
            print("\nPor favor, forneça uma frase para tradução.")
            return

        phrase_to_translate = " ".join(args)
        translator = Translator(to_lang="pt")
        translation = translator.translate(phrase_to_translate)

        print(f"\nTradução de '{phrase_to_translate}': {translation}")


class Converter(Command):
    async def execute(self, args: List[str]) -> None:
        imgs_suported = ["-jpg", "-jpeg", "-png", "-gif", "-bmp", "-webp"]
        videos_suported = ["-mp4", "-mkv", "-avi", "-mov", "-wmv", "-flv", "-webm"]
        audio_suported = ["-mp3", "-wav", "-flac", "-ogg", "-aac"]

        if not args:
            print("Por favor, forneça a extensão do arquivo a ser convertido.")
            return
        

        target_format = args[0]
        
        if not target_format.startswith("-"):
            print("Por favor, forneça a extensão do arquivo a ser convertido. Exemplo: convert -jpg caminho/arquivo.ext")
            return
        
        args = args[1:]

        # Verifica se o formato é suportado
        if (
            target_format in imgs_suported
            or target_format in videos_suported
            or target_format in audio_suported
        ):
            conversor = ConversorFactory.criar_conversor(target_format)
            conversor.convert(" ".join(args), target_format)
        else:
            print(f"Formato alvo {target_format} não suportado.")


class DownloadMusicCommand(Command):
    async def execute(self, args: List[str]) -> None:
        yt_downloader = YoutubeDownloader()
        if is_valid_url(" ".join(args)):
            yt_downloader.download_audio(" ".join(args))
        else:
            yt_search = YoutubeSearch()
            result = yt_search.search_one(" ".join(args))
            if isinstance(result, YouTube):
                yt_downloader.download_audio(result.watch_url)


class SearchYoutubeMusic(Command):
    async def execute(self, args: List[str]) -> None:
        yt_search = YoutubeSearch()
        result = yt_search.search_one(" ".join(args))
        if isinstance(result, YouTube):
            print(f"Título do vídeo: {result.title}")
            print(f"URL do vídeo: {result.watch_url}")
            print(f"Duração: {result.length}")


class HelpCommand(Command):
    def __init__(self, commands: list[CommandInfo]):
        self.commands = commands

    async def execute(self, args) -> None:
        print("\nComandos disponíveis:")
        for command in self.commands:
            print(f"\t{command}")
