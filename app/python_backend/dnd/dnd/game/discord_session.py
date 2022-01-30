from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv
import numpy as np
import discord
from discord.ext import commands

from dnd.game.runtime_library import RuntimeLibrary
from dnd.game.player import PlayerData
from dnd.game.session import Session
from typing import Optional, Dict, Any
import jsonpickle

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


class DiscordSession(commands.Bot):
    _lib: RuntimeLibrary
    _players: Dict[str, PlayerData]

    def __init__(self, command_prefix, self_bot, session: Session):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
        self._lib = session.lib
        self._players = session.players
        self.add_commands()

    @staticmethod
    def _format(obj: Any):
        return jsonpickle.encode(obj, unpicklable=False, indent=4)

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, name=GUILD)
        print(f'{self.user} is connected to the following guilds:\n')
        print(f'{guild.name} (id: {guild.id})')

    def add_commands(self):
        @self.command(name='r')
        async def roll_dice(context, content: str):
            if context.message.author == self.user:
                return

            print(f'Rolling dice from {content}')
            tokens = content.split('d')
            if len(tokens) != 2:
                return None
            count = int(tokens[0])
            tokens = tokens[1].split('+')
            die_size = int(tokens[0])
            extra = 0 if (len(tokens) == 1) else int(tokens[1])

            vals = np.random.randint(1, die_size + 1, size=(count,))
            await context.send(f'[{context.message.author.nick}] you rolled: '
                               f'({", ".join([str(ii) for ii in vals])}) + {extra} = {vals.sum() + extra}')

        @self.command(name='char')
        async def char(context, character_name: Optional[str]):
            if character_name is None:
                await context.send(self._lib.lib_keys('characters'))
                return

            try:
                await context.send(self._format(self._lib.get('characters', character_name)))
            except (KeyError, ValueError) as e:
                await context.send(f'got exception [{e}]')
                return

        @self.command(name='pl')
        async def player(context, player_name: Optional[str]):
            if player_name is None:
                await context.send(self._format([name for name in self._players]))
                return

            try:
                await context.send(self._format(self._players[player_name]))
            except (KeyError, ValueError) as e:
                await context.send(f'got exception [{e}]')
                return

        @self.command(name='lib')
        async def lib(context, lib_name: Optional[str], field_name: Optional[str]):
            try:
                if lib_name is None:
                    await context.send(self._format(self._lib.lib_names()))
                    return

                if field_name is None:
                    await context.send(self._format(self._lib.lib_keys(lib_name)))
                    return

                await context.send(self._format(self._lib.get(lib_name, field_name)))
            except KeyError:
                await context.send(f"Either lib name [{lib_name}] or field name [{field_name}] is invalid")


if __name__ == "__main__":
    bot = DiscordSession('>', False, Session.from_save_file(Path(os.path.dirname(__file__)).parent / 'savefile_2.zip'))
    bot.run(TOKEN)
