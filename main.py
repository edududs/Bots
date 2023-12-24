import asyncio

from commands.commands_core import CommandManager


class Bot:
    async def run(self):
        command_manager = CommandManager()

        while True:
            user_input = input("Digite um comando:")
            await command_manager.process_command(user_input)


if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.run())

