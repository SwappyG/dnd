import os

import re
import numpy as np
import json
import copy
import typing
import pprint


class DNDBot(commands.Bot):
    def __init__(self, command_prefix, self_bot):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
        self._lib = {}
        self._characters = {}

        for entry in os.scandir('players'):
            if entry.path.endswith(".json") and entry.is_file():
                with open(entry.path) as f:
                    self._characters[entry.name.split('.')[0]] = json.load(f)

        for entry in os.scandir('library'):
            if entry.path.endswith(".json") and entry.is_file():
                with open(entry.path) as f:
                    self._lib[entry.name.split('.')[0]] = json.load(f)

        self.add_commands()

    def add_commands(self):
        @self.command(name='r')
        async def roll_dice(context, content: str):
            if context.message.author == bot.user:
                return

            print(f'Rolling dice from {content}')
            tokens = content.split('d')
            if len(tokens) != 2:
                return None
            count = int(tokens[0])
            tokens = tokens[1].split('+')
            die_size = int(tokens[0])
            extra = 0 if (len(tokens) == 1) else int(tokens[1])

            vals = np.random.randint(1, die_size+1, size=(count,))
            await context.send(f'@{context.message.author.nick} you rolled: ({", ".join([str(ii) for ii in vals])}) + {extra} = {vals.sum() + extra}')

        def replace_from_library(character_data, lib_key):
            return { self._lib[lib_key][id]['name']: self._lib[lib_key][id] for id in character_data[lib_key] }

        @self.command(name='char')
        async def char(context, character_name: typing.Optional[str], category: typing.Optional[str]):
            if character_name is None:
                await context.send(pprint.pformat({k: self._characters[k]["level"] for k in self._characters}))
                return

            if character_name not in self._characters:
                await context.send(f'Character {character_name} is not in the game')
                return

            data = copy.deepcopy(self._characters[character_name])
            if category is not None:
                await context.send(f'{json.dumps(replace_from_library(data, category), indent=4)}')
                return

            data['weapons'] = replace_from_library(data, 'weapons')
            data['spells'] = replace_from_library(data, 'spells')
            data['items'] = replace_from_library(data, 'items')
            await context.send(f'{json.dumps(data, indent=4)}')

        @self.command(name='lib')
        async def lib(context, lib_name: typing.Optional[str], field_name: typing.Optional[str]):
            if lib_name is None:
                await context.send(pprint.pformat([ii for ii in self._lib]))                
                return 

            if field_name is None:
                await context.send(pprint.pformat([self._lib[lib_name][ii]['name'] for ii in self._lib[lib_name]]))
                return

            for entry in self._lib[lib_name]:
                print(entry)
                if self._lib[lib_name][entry]['name'] == field_name:
                    await context.send(json.dumps(self._lib[lib_name][entry], indent=4))
                    return
            
            await context.send(f'{field_name} was not found in {lib_name}')


    async def on_ready(self):
        guild = discord.utils.get(self.guilds, name=GUILD)
        print(f'{self.user} is connected to the following guilds:\n')
        print(f'{guild.name} (id: {guild.id})')


bot = DNDBot('>', self_bot=False)
bot.run(TOKEN)