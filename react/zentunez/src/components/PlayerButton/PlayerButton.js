import React from 'react';
import { MDBBtn } from "mdbreact";

export function PlayerButton(props) {
    return (
      <MDBBtn color="elegant" size="sm"
        onClick={ () => props.onClick() }
      >
        {props.caption}
      </MDBBtn>
    );
  }