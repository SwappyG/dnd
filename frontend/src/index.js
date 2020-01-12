import React from 'react';
import ReactDOM from 'react-dom';

import {PlayerPanel, PlayerListPanel} from './player.js'
import {Importer} from './importer.js'

class Game extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            currPlayer: null,
            players: []
        }
    }

    componentDidMount() {
        fetch('http://127.0.0.1:5000/players')
        .then(res => res.json())
        .then(data => {
          this.setState({ players: data })
        })
        .catch(err => {
            console.log(err)
        })
    }

    handlePlayerClick = (player) => {
        this.state.players.forEach(p => {
            if (p.name == player) {
                this.setState({currPlayer: <PlayerPanel player={p} />})
            }
        })
    }

    render() {
        return (
            <div>
                <div class="row mt-3">
                <div class="col-2" style={{"border-right": "1px solid #ccc"}}>
                    <PlayerListPanel players={this.state.players} onClick={this.handlePlayerClick} />
                </div>
                <div class="col-10">
                    {this.state.currPlayer}
                </div>
                </div>
                <div class="row mt-3">
                    <div class="col">
                        <Importer />
                    </div>
                </div>
            </div>
        );
    }
}

ReactDOM.render(
    <Game />,
    document.getElementById('root')
);
  