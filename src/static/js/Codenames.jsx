import React from 'react';
import styled from 'styled-components';

import Roomselect from './Roomselect';
import Userselect from './Userselect';
import GameTable from './GameTable';

export const Teams = {
    SPECTATOR: "spectator",
    BLUE: "blue",
    RED: "red"
};

export default class Codenames extends React.Component {
    constructor(props) {
        super(props);
        this.state =
            { roomId: '', currentUser: '', currentTeam: Teams.SPECTATOR };
    }

    render() {
        return (
            <Container>
                {this.getPage()}
            </Container>
        );
    }

    getPage = () => {
        const { roomId, currentUser } = this.state;
        if (!roomId) {
            return <Roomselect baseURL={this.props.baseURL} setRoomId={this.setRoomId} />
        }
        if (!currentUser) {
            // return <user/team select>
            return <Userselect baseURL={this.props.baseURL} roomId={roomId} setCurrentUser={this.setCurrentUser} />
        }
        return this.getGame();
    };

    getGame = () => {
        const { roomId, currentUser, currentTeam } = this.state;
        return (
            <div>
                <div>roomId = {roomId}</div>
                <div>user = {currentUser}</div>
                <div>team = {currentTeam}</div>
                <GameTable
                    baseURL={this.props.baseURL}
                    roomId={roomId}
                    user={currentUser}
                    team={currentTeam}
                />
            </div>
        );
    };

    setRoomId = (id) => {
        this.setState({ roomId: id });
    };

    setCurrentUser = (user, team) => {
        this.setState({ currentUser: user, currentTeam: team });
    };

}
const Container = styled.div(() => {
    return {
        display: 'flex',
        justifyContent: 'center',
    }
});

