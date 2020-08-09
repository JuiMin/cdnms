import React from 'react';
import styled from 'styled-components';

export default class Codenames extends React.Component {
    render() {
        return <Container>Why cant I, hold all these codenames?</Container>;
    }
}
const Container = styled.div(() => {
    return {
        border: '1px solid blue'
    }
})
