import React, { Component } from 'react';
import {Divider} from "../Divider/Divider.js"


export class PlayerState extends Component {
    /**
     * This component handles the display of the album cover, along with a
     * button to update it
     */
    constructor(props) {
      super(props);
      this.state = {artist: "",
                    album: "",
                    track: "",
                    volume: 0,
                    state: "",
                    position: 0.0 };
    };
    
    render(){
      return (
        <div>
          <p><b>Artist :</b> { this.state.artist }</p>
          <Divider />
          <p><b>Album :</b> { this.state.album }</p>
          <Divider />
          <p><b>Track :</b> { this.state.track }</p>
          <Divider />
          <p><b>State :</b> { this.state.state }</p>
          <Divider />
          <p><b>Volume :</b> { parseInt(100 * this.state.volume) }</p>
          <Divider />
          <p><b>Position :</b> { parseInt(100 * this.state.state) }</p>
        </div>
      );
    }
  }