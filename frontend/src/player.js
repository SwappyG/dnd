import React from 'react';
import {StatPanel} from './stats.js'
import {ItemPanel} from './items.js'
import {FeaturePanel} from './features.js'

class PlayerInfoBar extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div class="row">
                <div class="col-2">
                    <h3>{this.props.name}</h3>
                </div>
                <div class="col-6">
                    <h3>{this.props.job}</h3>
                </div>
                <div class="col-2">
                    <h3>{this.props.level}</h3>
                </div>
                <div class="col-2">
                    <h3>{this.props.gender}{this.props.age}</h3>  
                </div>
            </div>
        );
    }
}

export class PlayerPanel extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div>
                <PlayerInfoBar name={this.props.player.name} job={this.props.player.job} level={this.props.player.level} gender={this.props.player.gender} age={this.props.player.age} />
                <hr></hr>
                <div class="row">
                    <div class="col-2" style={{"border-right": "1px solid #ccc"}}>
                        <StatPanel playerName={this.props.player.name} regStats={this.props.player.regStats} basicStats={this.props.player.basicStats} />
                    </div>
                    <div class="col-10">
                        <div class="ml-2">
                            <div class="mb-3">
                                <ItemPanel playerName={this.props.player.name} equiped={this.props.player.items.equiped} inventory={this.props.player.items.inventory}/>
                            </div>
                            <div>
                                <FeaturePanel playerName={this.props.player.name} features={this.props.player.features} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export class PlayerListPanel extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div>
                <h2>Players</h2>
                {this.props.players.map(player => (
                    <button class="btn btn-secondary btn-block" onClick={() => this.props.onClick(player.name)}>{player.name}</button>
                ))}
            </div>
        );
    }
}