import React, { Component } from 'react';
import './TrackList.css';

export class TrackList extends Component {
    /**
     * This component handles the display of the track list for an album
     */

    render(){
      return (
        <div className="track-list" >
            { this.props.tracks.map((item, index) => (
                <li key={index}>{item}</li>
            ))}
        </div>
      );
    }
  }