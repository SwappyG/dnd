import React from 'react';

export class FeaturePanel extends React.Component {
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