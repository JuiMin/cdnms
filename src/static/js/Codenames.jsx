import React from 'react';
import styled from 'styled-components';

import { get, post } from './util/http'

export default class Codenames extends React.Component {
    constructor(props) {
        super(props);
        this.state =
            { newRoomName: '', existingRoomName: '', roomId: '', };
    }

    render() {
        return (
            <Container>
                {this.getGame()}
            </Container>
        );
    }

    // return the items needed for the state of the game
    getGame = () => {
        if (!this.state.roomId) {
            return (
                <Game>
                    <div>
                        <InputContainer placeholder="room name" onChange={this.handleNewRoomInput}></InputContainer>
                        <ButtonContainer onClick={this.createRoom}>Create a room</ButtonContainer>
                    </div>
                    <div>
                        <InputContainer placeholder="room name" onChange={this.handleExistingRoomInput}></InputContainer>
                        <ButtonContainer onClick={this.joinRoom}>Or join an existing one</ButtonContainer>
                    </div>
                </Game>
            )
        }
        // TODO: return actual game with board/players/controls
        return <Game>
            roomId is {this.state.roomId}
        </Game>
    }

    // NEW ROOM STUFF
    handleNewRoomInput = (e) => {
        e.preventDefault();
        this.setState({ newRoomName: e.target.value });
    }

    createRoom = (e) => {
        if (this.state.newRoomName) {
            post(baseURL + "rooms", undefined, { name: this.state.newRoomName }, this.onCreateRoomSuccess, this.onFailure);
        } else {
            alert('please enter a room name');
        }
    };

    onCreateRoomSuccess = (response) => {
        console.log('created room with name', this.state.newRoomName);
        // load room
        this.setState({ roomId: this.state.newRoomName });
    }

    // EXISTING ROOM STUFF
    handleExistingRoomInput = (e) => {
        e.preventDefault();
        this.setState({ existingRoomName: e.target.value });
    }

    joinRoom = (e) => {
        const { existingRoomName } = this.state;
        if (existingRoomName) {
            console.log('joining', existingRoomName);
            console.log('url:', baseURL + "rooms/" + existingRoomName);
            post(baseURL + "rooms/" + existingRoomName, undefined, { 'action': 'test' }, this.onJoinRoomSuccess, this.onFailure);
        } else {
            alert('please enter a room name');
        }
    };

    onJoinRoomSuccess = (response) => {
        console.log('joining room', this.state.existingRoomName);
        // load room
        this.setState({ roomId: this.state.existingRoomName });
    }

    onFailure = (error) => {
        alert(error + ". Try again.");
    }

}
const Container = styled.div(() => {
    return {
        display: 'flex',
        justifyContent: 'center',
    }
});

const Game = styled.div(() => {
    return {}
});

const ButtonContainer = styled.button(() => {
    return {}
});

const InputContainer = styled.input(() => {
    return {};
});

