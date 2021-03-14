from __future__ import annotations

import os
from pathlib import Path
from dnd.game.runtime_library import RuntimeLibrary
from dnd.game.player import PlayerData
from dnd.game.session import Session
from dnd.utils.importer import load_test_data
from typing import Dict, List

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import jsonpickle


class FlaskSession:
    _lib: RuntimeLibrary
    _players: Dict[str, PlayerData]

    def __init__(self, session: Session):
        self._app = Flask(__name__)
        self._cors = CORS(self._app)
        self._lib = session.lib
        self._players = session.players
        self.add_commands()

    def run(self):
        self._app.run(host='localhost', port=8080)

    def _get_lib_as_list(self, lib_name: str):
        lib = self._lib.get_lib(lib_name)
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
    lib, players = load_test_data()
    app = FlaskSession(Session(lib=RuntimeLibrary(lib), players_list=players))
    app.run()
