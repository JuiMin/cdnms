import React from 'react';
import { Teams } from './Codenames';

import { post } from './util/http'

export default class Userselect extends React.Component {
    constructor(props) {
        super(props);
        this.state =
            { currentUser: '', team: Teams.SPECTATOR };
    }

    render() {
        return this.getComponent();
    }

    getComponent = () => {
        return (
            <div>
                <label htmlFor="username">Enter a username:</label>
                <input id="username" placeholder="username" onChange={this.handleUserInput}></input>
                <label htmlFor="team">Pick a team:</label>
                <select id="team" onChange={this.handleDropdown}>
                    <option value={Teams.SPECTATOR}>Spectator</option>
                    <option value={Teams.RED}>Red</option>
                    <option value={Teams.BLUE}>Blue</option>
                </select>
                <button onClick={this.createUser}>Submit</button>
            </div>
        )
    }

    handleUserInput = (e) => {
        e.preventDefault();
        this.setState({ currentUser: e.target.value });
    }

    handleDropdown = (e) => {
        e.preventDefault();
        this.setState({ team: e.target.value });
    }

    createUser = (e) => {
        const { baseURL, roomId } = this.props;
        const requestBody = {
            name: this.state.currentUser,
            team: this.state.team
        };
        if (this.state.currentUser && this.state.team) {
            post(baseURL + 'rooms/' + roomId + '/' + 'players', undefined, requestBody, this.onUserCreate, this.onFailure);
        } else {
            alert('please enter a username and team');
        }
    };

    onUserCreate = (response) => {
        let team = this.state.team;
        this.props.setCurrentUser(this.state.currentUser, team);
    };

    onFailure = (error) => {
        alert(error + ". Try again.");
    }

}

