import React from 'react';
import styled from 'styled-components';

import Roomselect from './Roomselect';

export default class Codenames extends React.Component {
    constructor(props) {
        super(props);
        this.state =
            { roomId: '', };
    }

    render() {
        return (
            <Container>
                {this.getGame()}
            </Container>
        );
    }

    getGame = () => {
        const { roomId } = this.state;
        if (!roomId) {
            return <Roomselect baseURL={this.props.baseURL} setRoomId={this.setRoomId} />
        }
        return <div>roomId = {roomId}</div>
    };

    setRoomId = (id) => {
        this.setState({ roomId: id });
    };

}
const Container = styled.div(() => {
    return {
        display: 'flex',
        justifyContent: 'center',
    }
});

