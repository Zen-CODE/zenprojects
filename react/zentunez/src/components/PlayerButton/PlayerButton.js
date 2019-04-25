import React, { Component } from 'react';
import {Divider} from "../Divider/Divider.js"

export function PlayerButton(props) {
    return (
      <button
        className="PlayerButton"
        api_call={props.api_call}
        onClick={() => props.callback(props.api_call)}
      >
        {props.caption}
      </button>
    );
  }