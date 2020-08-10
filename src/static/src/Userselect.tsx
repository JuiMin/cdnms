import React from 'react';
import { Team } from './Codenames';

import { post } from './util/http'

export interface UserselectProps {
    baseURL: string;
    roomId: string;
    setCurrentUser: (user: string, team: Team) => void;
}

export interface UserselectState {
    currentUser: string;
    team: Team;
}

export default class Userselect extends React.Component<UserselectProps, UserselectState> {
    constructor(props: UserselectProps) {
        super(props);
        this.state =
            { currentUser: '', team: 'Spectator' };
    }

    public render(): React.ReactNode {
        return this.getComponent();
    }

    private readonly getComponent = (): React.ReactNode => {
        return (
            <div>
                <label htmlFor="username">Enter a username:</label>
                <input id="username" placeholder="username" onChange={this.handleUserInput}></input>
                <label htmlFor="team">Pick a team:</label>
                <select id="team" onChange={this.handleDropdown}>
                    <option value={'Spectator'}>Spectator</option>
                    <option value={'Red'}>Red</option>
                    <option value={'Blue'}>Blue</option>
                </select>
                <button onClick={this.createUser}>Submit</button>
            </div>
        )
    }

    private readonly handleUserInput = (e: React.ChangeEvent<HTMLInputElement>): void => {
        e.preventDefault();
        const target = e.target as HTMLInputElement;
        this.setState({ currentUser: target.value });
    }

    private readonly handleDropdown = (e: React.ChangeEvent<HTMLSelectElement>): void => {
        e.preventDefault();
        const target = e.target as HTMLSelectElement;
        // we set the values, so we know they are of type Team but feels dirty
        this.setState({ team: target.value as Team });
    }

    private readonly createUser = (e: React.MouseEvent<HTMLButtonElement>): void => {
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

    private readonly onUserCreate = (response: any): void => {
        this.props.setCurrentUser(this.state.currentUser, this.state.team);
    };

    private readonly onFailure = (error: Error): void => {
        alert(error + ". Try again.");
    }

}

