from __future__ import annotations

import os
from pathlib import Path
from dnd.game.runtime_library import RuntimeLibrary
from dnd.game.player import PlayerData
from dnd.game.game import Game
from dnd.utils.importer import load_test_data
from typing import Dict, List

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import jsonpickle


class FlaskSession:
    _game: Game

    def __init__(self, game: Game):
        self._app = Flask(__name__)
        self._cors = CORS(self._app)
        self._game = game
        self.add_commands()

    def run(self):
        self._app.run(host='localhost', port=8080)

    def _get_lib_as_list(self, lib_name: str):
        lib = self._game._runtime_lib.get_lib(lib_name)
        return self._app.response_class(
            response=jsonpickle.encode({'data': [e.as_dict() for e in lib]}, unpicklable=False),
            status=200,
            mimetype='application/json'
        )

    def add_commands(self):
        @self._app.route('/library/<lib_name>', methods=['GET'])
        def get_from_library(lib_name: str):
            return self._get_lib_as_list(lib_name)


if __name__ == "__main__":
    library, player_data_list = load_test_data()
    app = FlaskSession(Game(library, player_data_list))
    app.run()
