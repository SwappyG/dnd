import React from 'react';
import ReactDOM from 'react-dom';


class Decrement extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <i class="fa fa-chevron-left fa-2" onClick={this.props.onclick}></i>
        );
    }
}

class Increment extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <i class="fa fa-chevron-right fa-2" onClick={this.props.onclick}></i>
        );
    }
}

class Number extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            value: this.props.value
        }
    }

    render() {
        return (
            <div class="row">
                <div class="col">
                    <Decrement onclick={this.props.onDecrement} />
                </div>
                <div class="col">
                    {this.state.value}
                </div>
                <div class="col">
                    <Increment onclick={this.props.onIncrement} />
                </div>
            </div>
        );
    }
}

class Trash extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <i class="fa fa-trash fa-2 mr-2"></i>
        );
    }
}

class Item extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div class="row">
                <div class="col-1">
                    <Trash onclick={() => this.props.handleTrashClick(this.props.name)}/>
                </div>
                <div class="col-8">
                    {this.props.name}
                </div>
                <div class="col-3">
                    <Number value={this.props.quantity} 
                            onDecrement={() => this.props.onDecrement(this.props.name)} 
                            onIncrement={() => this.props.onIncrement(this.props.name)} />
                </div>
            </div>
        );
    }
}

class ItemPanel extends React.Component {
    constructor(props) {
        super(props)
        this.state = {showEquiped: true};
    }

    handleEquipedClick = () => {
        this.setState({showEquiped: true});
    }
    
    handleInventoryClick = () => {
        this.setState({showEquiped: false});
    }

    handleDecrementClick = (itemName) => {
        // do post req
        this.setState({})
    }

    handleIncrementClick = (itemName) => {
        // do post req
        this.setState({})
    }

    handleTrashClick = (itemName) => {
        // do post req
        this.setState({})
    }

    render() {
        let items;
        if (this.state.showEquiped) {
            items = this.props.equiped
        } else {
            items = this.props.inventory
        }

        return (
            <div>
                <div class="row">
                    <h2>Items</h2>
                </div>
                <div class="row">
                    <div class="btn-group">
                        <button class="btn btn-secondary ml-3 mr-1" onClick={this.handleEquipedClick}>Equiped</button>
                        <button class="btn btn-secondary" onClick={this.handleInventoryClick}>Inventory</button>
                    </div>
                </div>
                <div>
                    {items.map(item => (
                        <Item name={item.name} quantity={item.quantity} onDecrement={this.handleDecrementClick} onIncrement={this.handleIncrementClick} />
                    ))}
                </div>
            </div>
        );
    }
}

class Stat extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div class="row">
                <div class="col">
                    {this.props.skillName}
                </div>
                <div class="col">
                    {this.props.skillValue}
                </div>
            </div>
        );
    }
}

class StatPanel extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div>
                {this.props.regStats.map(skill => (
                    <Stat skillName="str" skillValue="99" />
                ))}
                <hr></hr>
                {this.props.basicStats.map(skill => (
                    <Stat skillName="str" skillValue="99" />
                ))}
            </div>
        );
    }
}

class FeaturePanel extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            description: null
        }
    }
    
    handleFeatureClick = (featureName) => {
        this.props.features.forEach(f => {
            if (f.name === featureName) {
                this.setState({description: f.description})
            }
        });
    }

    render() {
        return (
            <div onclick={this.handleFeatureClick}>
                <div class="row">
                    <h2>Features</h2>
                </div>
                <div class="row">
                    <div class="col-3 overflow-auto" style={{height: 150}}>
                        {this.props.features.map(feature => (               
                            <h6 onClick={() => this.handleFeatureClick(feature.name)}>{feature.name}</h6>
                        ))}
                    </div>
                    <div class="col-9 overflow-auto" style={{height: 150}}>
                        <p>
                            {this.state.description}
                        </p>
                    </div>
                </div>
            </div>
        );
    }
}

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

class PlayerPanel extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div>
                <PlayerInfoBar name={this.props.player.name} job={this.props.player.job} level={this.props.player.level} gender={this.props.player.gender} age={this.props.player.age} />
                <hr></hr>
                <div class="row">
                    <div class="col-2">
                        <StatPanel playerName={this.props.player.name} regStats={this.props.player.regStats} basicStats={this.props.player.basicStats} />
                    </div>
                    <div class="col-10">
                    <ItemPanel playerName={this.props.player.name} equiped={this.props.player.items.equiped} inventory={this.props.player.items.inventory}/>
                    <FeaturePanel playerName={this.props.player.name} features={this.props.player.features} />
                    </div>
                </div>
            </div>
        );
    }
}

class PlayerListPanel extends React.Component {
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


class Main extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            currPlayer: null
        }
    }

    handlePlayerClick = (player) => {
        this.props.players.forEach(p => {
            if (p.name == player) {
                this.setState({currPlayer: <PlayerPanel player={p} />})
            }
        })
    }

    render() {
        return (
            <div class="row">
                <div class="col-2">
                    <PlayerListPanel players={this.props.players} onClick={this.handlePlayerClick} />
                </div>
                <div class="col-10">
                    {this.state.currPlayer}
                </div>
            </div>
            
        );
    }
}
  
// ========================================

let players = [
    {
        name: 'P1',
        job: 'Job1',
        level: '10',
        gender: 'M',
        age: '20',
        items: {
            equiped: [
                {
                    name: 'item1',
                    quantity: 5
                },
                {
                    name: 'item2',
                    quantity: 5
                },
            ],
            inventory: [
                {
                    name: 'item3',
                    quantity: 5
                },
                {
                    name: 'item4',
                    quantity: 5
                },
                {
                    name: 'item6',
                    quantity: 5
                },
                {
                    name: 'item7',
                    quantity: 5
                },
            ]
        },
        features: [
            {
                name: 'feature1',
                description: 'description1'
            },
            {
                name: 'feature2',
                description: 'description1'
            },
            {
                name: 'feature3',
                description: 'description1'
            },
        ],
        regStats: [
            {name: 'str', quantity: 10},
            {name: 'atk', quantity: 17},
            {name: 'dex', quantity: 11},
            {name: 'int', quantity: 12},
        ],
        basicStats: [
            {name: 'hp', quantity: 66},
            {name: 'acr', quantity: 4},
        ]
    },
]

ReactDOM.render(
    <Main players={players}/>,
    document.getElementById('root')
);
  