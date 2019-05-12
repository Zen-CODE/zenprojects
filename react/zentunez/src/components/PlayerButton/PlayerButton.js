import React from 'react';
import { MDBBtn } from "mdbreact";

export function PlayerButton(props) {
    return (
      <MDBBtn color="primary" size="sm"
        onClick={ () => props.onClick() }
      >
        {props.caption}
      </MDBBtn>
    );
  }