import React from 'react';

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

export class ItemPanel extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            showEquiped: true,
            equiped: props.equiped,
            inventory: props.inventory
        };
    }

    handleEquipedClick = () => {
        this.setState({showEquiped: true});
    }
    
    handleInventoryClick = () => {
        this.setState({showEquiped: false});
    }

    handleDecrementClick = (itemName) => {
        fetch('http://localhost:5000/player/items/decrement', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'name': itemName,
                'playerName': this.props.playerName
            })
        })
        .then(res => res.json())
        .then(data => {
          this.setState({ items: data })
        })
        .catch(err => {
            console.log(err)
        })
    }

    handleIncrementClick = (itemName) => {
        fetch('http://localhost:5000/player/items/increment', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'name': itemName,
                'playerName': this.props.playerName
            })
        })
        .then(res => res.json())
        .then(data => {
          this.setState({ items: data })
        })
        .catch(err => {
            console.log(err)
        })
    }

    handleTrashClick = (itemName) => {
        fetch('http://localhost:5000/player/items/delete', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'name': itemName,
                'playerName': this.props.playerName
            })
        })
        .then(res => res.json())
        .then(data => {
          this.setState({ items: data })
        })
        .catch(err => {
            console.log(err)
        })
    }

    render() {
        let items;
        if (this.state.showEquiped) {
            items = this.state.equiped
        } else {
            items = this.state.inventory
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
                <div class="overflow-auto" style={{"height": 200}}>
                    {items.map(item => (
                        <Item name={item.name} quantity={item.quantity} onDecrement={this.handleDecrementClick} onIncrement={this.handleIncrementClick} />
                    ))}
                </div>
            </div>
        );
    }
}