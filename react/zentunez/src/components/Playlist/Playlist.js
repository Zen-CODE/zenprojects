import React, { Component } from 'react';
import '../TrackList/TrackList.css';
import { queued_fetch } from "../../functions/network.js"


export class Playlist extends Component {
    /**
     * This component handles the display of the track list for an album
     */
    constructor(props) {
        super(props);

        this.state = {
                    api_url: props.api_url,
                    tracks: [],
                    track: ""};
        this.setPlaylist();
    };


    componentDidUpdate(prevProps){
      // When the tracks changes, load the new playlist
      console.log("PLaylist: componentDidUpdate.");
      if (this.props.track !== prevProps.track) {
        this.setPlaylist()
      }
    }

    setPlaylist() {
      /* Load and set the current playlist  */
        console.log("Playlist: Fetching tracks");
        const set_state = (response) => {
            console.log("Got playlist. track = " + this.state.track);
            this.setState({tracks: response})
        };
        queued_fetch(this.state.api_url + "zenplaylist/get_playlist", set_state)
    }


    render(){
      return (
        <div className="track-list no-bullet" >
          <div className="track-separator" />
          <b>Playlist</b>
          <div className="track-separator" />
          {/* Track listing */}
          { this.state.tracks.map((item, index) => (
                <li className={ !item.text.includes(this.state.track) ? "active-track": "" } key={index} >{item.text}</li>
          ))}
        </div>
      );
    }
  }
