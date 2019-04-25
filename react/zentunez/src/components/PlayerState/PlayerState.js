import React, { Component } from 'react';


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
          <p><b>Volume :</b> { parseInt(100 * this.props.volume) }</p>
          <p><b>Position :</b> { parseInt(100 * this.props.state) }</p>
        </div>
      );
    }
  }