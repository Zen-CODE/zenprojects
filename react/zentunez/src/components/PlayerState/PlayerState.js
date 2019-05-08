import React, { Component } from 'react';
import './PlayerState.css';

export class PlayerState extends Component {
    /**
     * This component handles the display of the album cover, along with a
     * button to update it
     */    
    render(){
      return (
        <div>
          <p><b>Artist :</b> { this.props.artist }</p>
          <p><b>Album :</b> { this.props.album }</p>
          <p><b>Track :</b> { this.props.track }</p>
          <p><b>State :</b> { this.props.state }</p>
          <input type="range" min="0" max="100" value={ this.props.position * 100 } readOnly={ true }/>
          <br />
          <img className="album-cover" alt="Album cover" src={ this.props.img_src }></img>
        </div>
      );
    }
  }