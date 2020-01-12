import React from 'react';

export class Title extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <h2>{this.props.value}</h2>
        );
    }
}

export class Paragraph extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <p>{this.props.value}</p>
        );
    }
}