import React from 'react';

class Stat extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div class="row">
                <div class="col">
                    {this.props.name}
                </div>
                <div class="col">
                    {this.props.value}
                </div>
            </div>
        );
    }
}

export class StatPanel extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div>
                {this.props.regStats.map(stat => (
                    <Stat name={stat.name} value={stat.quantity} />
                ))}
                <hr></hr>
                {this.props.basicStats.map(stat => (
                    <Stat name={stat.name} value={stat.quantity} />
                ))}
            </div>
        );
    }
}