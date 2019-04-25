import React, { Component } from 'react';
import {Divider} from "../Divider/Divider.js"


export class PlayerState extends Component {
    /**
     * This component handles the display of the album cover, along with a
     * button to update it
     */    
    render(){
      return (
        <div>
          <p><b>Artist :</b> { this.props.artist }</p>
          <Divider />
          <p><b>Album :</b> { this.props.album }</p>
          <Divider />
          <p><b>Track :</b> { this.props.track }</p>
          <Divider />
          <p><b>State :</b> { this.props.state }</p>
          <Divider />
          <p><b>Volume :</b> { parseInt(100 * this.props.volume) }</p>
          <Divider />
          <p><b>Position :</b> { parseInt(100 * this.props.state) }</p>
        </div>
      );
    }
  }