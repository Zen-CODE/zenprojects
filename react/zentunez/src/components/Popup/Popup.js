import React, { Component } from 'react';
import { MDBContainer, MDBBtn, MDBModal, MDBModalBody, MDBModalHeader, MDBModalFooter } from 'mdbreact';

export class Popup extends Component {
state = {
  modal: false,
  title: "Title",
  body: "Body",
}

toggle = () => {
  this.setState({
    modal: !this.state.modal,
  });
}

render() {
  return (
    <MDBContainer>
      <MDBBtn onClick={this.toggle}>Modal</MDBBtn>
      <MDBModal isOpen={this.state.modal} toggle={this.toggle}>
        <MDBModalHeader toggle={this.toggle}>{ this.state.title }</MDBModalHeader>
        <MDBModalBody>
          { this.state.body }
        </MDBModalBody>
        <MDBModalFooter>
          <MDBBtn color="primary" onClick={this.toggle}>Close</MDBBtn>
        </MDBModalFooter>
      </MDBModal>
    </MDBContainer>
    );
  }
}
