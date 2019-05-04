import React, { Component } from 'react';
import './Library.css';
import { VDivider } from '../Divider/Divider.js'

export class Library extends Component {
    /**
     * This component displays the volume slider
     */    
    constructor(props) {
        super(props);
        this.state = {
          artist: "-",
          album: "-",
          img_src: ""
        }
      };  

    Click() {
      console.log("I Have been clicked")

    }


    render(){
      return (
        <div className="LibraryPanel">
          <p><b>ZenTunez Library</b></p>
          <VDivider />
          <p><b>Artist:</b>{ this.artist } </p>
          <p><b>Album:</b>{ this.album } </p>
          <VDivider />
          <img className="album-cover" alt="Album cover" src={ this.props.img_src }></img>
          <br />
          <VDivider />
          <button onClick={() => this.Click()}>Random album</button>
        </div>
      );
    }
  }