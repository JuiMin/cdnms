import React from "react";

import { post } from "./util/http";

export interface RoomselectProps {
  baseURL: string;
  setRoomId: (id: string) => void;
}

export interface RoomselectState {
  newRoomName: string;
  existingRoomName: string;
}

export default class Roomselect extends React.Component<
  RoomselectProps,
  RoomselectState
> {
  constructor(props: RoomselectProps) {
    super(props);
    this.state = { newRoomName: "", existingRoomName: "" };
  }

  public render(): React.ReactNode {
    return this.getComponent();
  }

  private readonly getComponent = (): React.ReactNode => {
    return (
      <div>
        <div>
          <input
            placeholder="room name"
            onChange={this.handleNewRoomInput}
          ></input>
          <button onClick={this.createRoom}>Create a room</button>
        </div>
        <div>
          <input
            placeholder="room name"
            onChange={this.handleExistingRoomInput}
          ></input>
          <button onClick={this.joinRoom}>Or join an existing one</button>
        </div>
      </div>
    );
  };

  // NEW ROOM STUFF
  private readonly handleNewRoomInput = (
    e: React.ChangeEvent<HTMLInputElement>
  ): void => {
    e.preventDefault();
    const target = e.target as HTMLInputElement;
    this.setState({ newRoomName: target.value });
  };

  private readonly createRoom = (
    e: React.MouseEvent<HTMLButtonElement>
  ): void => {
    if (this.state.newRoomName) {
      post(
        this.props.baseURL + "rooms",
        undefined,
        { name: this.state.newRoomName },
        this.onCreateRoomSuccess,
        this.onFailure
      );
    } else {
      alert("please enter a room name");
    }
  };

  private readonly onCreateRoomSuccess = (response: any): void => {
    console.log("created room with name", this.state.newRoomName);
    // load room
    this.props.setRoomId(this.state.newRoomName);
  };

  // EXISTING ROOM STUFF
  private readonly handleExistingRoomInput = (
    e: React.ChangeEvent<HTMLInputElement>
  ): void => {
    e.preventDefault();
    const target = e.target as HTMLInputElement;
    this.setState({ existingRoomName: target.value });
  };

  private readonly joinRoom = (
    e: React.MouseEvent<HTMLButtonElement>
  ): void => {
    const { existingRoomName } = this.state;
    if (existingRoomName) {
      post(
        this.props.baseURL + "rooms/" + existingRoomName,
        undefined,
        { action: "test" },
        this.onJoinRoomSuccess,
        this.onFailure
      );
    } else {
      alert("please enter a room name");
    }
  };

  private readonly onJoinRoomSuccess = (response: any): void => {
    console.log("joined room", this.state.existingRoomName);
    // load room
    this.props.setRoomId(this.state.existingRoomName);
  };

  private readonly onFailure = (error: Error): void => {
    alert(error + ". Try again.");
  };
}
