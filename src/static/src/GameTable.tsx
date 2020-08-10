import React from "react";
import { Team } from "./Codenames";

export interface GameTableProps {
  baseURL: string;
  roomId: string;
  user: string;
  team: Team;
}

export interface GameTableState {
  isLoading: boolean;
}

export default class GameTable extends React.Component<
  GameTableProps,
  GameTableState
> {
  constructor(props: GameTableProps) {
    super(props);
    this.state = { isLoading: true };
  }

  public render(): React.ReactNode {
    return this.getComponent();
  }

  public componentDidMount = (): void => {
    setTimeout(() => this.setState({ isLoading: false }), 5000);
  };

  private readonly getComponent = (): React.ReactNode => {
    return this.state.isLoading ? (
      <div>loading card games on motorcycles, please wait...</div>
    ) : (
      this.getCards()
    );
  };

  private readonly getCards = (): React.ReactNode => {
    return <div>surprise, IS THIS YOUR CARD?</div>;
  };
}
