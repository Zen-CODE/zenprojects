import React, { Component } from 'react';
import './TrackList.css';

export class TrackList extends Component {
    /**
     * This component handles the display of the track list for an album
     */
    constructor(props) {
        super(props);
        this.state = {tracks: ["Test track1", "Test track 2"]};
      };

    render(){
      return (
        <div className="track-list" >
            { this.state.tracks.map((item, index) => (
                <li key={index}>{item}</li>
            ))}
        </div>
      );
    }
  }