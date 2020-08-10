import React from 'react';
import Teams from './Codenames';

import { post } from './util/http'

export default class GameTable extends React.Component {
    constructor(props) {
        super(props);
        this.state =
            { isLoading: true };
    }

    render() {
        return this.getComponent();
    }

    componentDidMount = () => {
        setTimeout(() => this.setState({ isLoading: false }), 5000);
    }

    getComponent = () => {
        return this.state.isLoading ? (
            <div>
                loading card games on motorcycles, please wait...
            </div>
        ) : this.getCards();
    }

    getCards = () => {
        return (
            <div>
                surprise, IS THIS YOUR CARD?
            </div>
        )
    }

}

