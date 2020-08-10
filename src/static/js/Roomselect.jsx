import React from 'react';

import { post } from './util/http'

export default class Roomselect extends React.Component {
    constructor(props) {
        super(props);
        this.state =
            { newRoomName: '', existingRoomName: '', };
    }

    render() {
        return this.getComponent();
    }

    getComponent = () => {
        return (
            <div>
                <div>
                    <input placeholder="room name" onChange={this.handleNewRoomInput}></input>
                    <button onClick={this.createRoom}>Create a room</button>
                </div>
                <div>
                    <input placeholder="room name" onChange={this.handleExistingRoomInput}></input>
                    <button onClick={this.joinRoom}>Or join an existing one</button>
                </div>
            </div>
        )
    }

    // NEW ROOM STUFF
    handleNewRoomInput = (e) => {
        e.preventDefault();
        this.setState({ newRoomName: e.target.value });
    }

    createRoom = (e) => {
        if (this.state.newRoomName) {
            post(this.props.baseURL + "rooms", undefined, { name: this.state.newRoomName }, this.onCreateRoomSuccess, this.onFailure);
        } else {
            alert('please enter a room name');
        }
    };

    onCreateRoomSuccess = (response) => {
        console.log('created room with name', this.state.newRoomName);
        // load room
        this.props.setRoomId(this.state.newRoomName);
    }

    // EXISTING ROOM STUFF
    handleExistingRoomInput = (e) => {
        e.preventDefault();
        this.setState({ existingRoomName: e.target.value });
    }

    joinRoom = (e) => {
        const { existingRoomName } = this.state;
        if (existingRoomName) {
            post(this.props.baseURL + "rooms/" + existingRoomName, undefined, { 'action': 'test' }, this.onJoinRoomSuccess, this.onFailure);
        } else {
            alert('please enter a room name');
        }
    };

    onJoinRoomSuccess = (response) => {
        console.log('joined room', this.state.existingRoomName);
        // load room
        this.props.setRoomId(this.state.existingRoomName);
    }

    onFailure = (error) => {
        alert(error + ". Try again.");
    }

}

