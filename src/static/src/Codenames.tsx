import React from 'react';
import styled from 'styled-components';

import Roomselect from './Roomselect';
import Userselect from './Userselect';
import GameTable from './GameTable';

export type Team = 'Spectator' | 'Blue' | 'Red';

export interface CodenamesProps {
    baseURL: string;
}

export interface CodenamesState {
    roomId: string;
    currentUser: string;
    currentTeam: Team;
}

export default class Codenames extends React.Component<CodenamesProps, CodenamesState> {
    constructor(props: CodenamesProps) {
        super(props);
        this.state =
            { roomId: '', currentUser: '', currentTeam: 'Spectator' };
    }

    public render(): React.ReactNode {
        return (
            <Container>
                {this.getPage()}
            </Container>
        );
    }

    private readonly getPage = (): React.ReactNode => {
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

    private readonly getGame = (): React.ReactNode => {
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

    private readonly setRoomId = (id: string): void => {
        this.setState({ roomId: id });
    };

    private readonly setCurrentUser = (user: string, team: Team): void => {
        this.setState({ currentUser: user, currentTeam: team });
    };

}
const Container = styled.div(() => {
    return {
        display: 'flex',
        justifyContent: 'center',
    }
});

