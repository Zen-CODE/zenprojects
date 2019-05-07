import React, { Component } from 'react';

export class TrackList extends Component {
    /**
     * This component handles the display of the track list for an album
     */
    constructor(props) {
        super(props);
        this.state = {tracks: ["test track1", "Test track 2"]};
      };

    render(){
      return (
        <div>
            { this.state.tracks.map((item, index) => (
                <li key={index}>{item}</li>
            ))}
        </div>
      );
    }
  }