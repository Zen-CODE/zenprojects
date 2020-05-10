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
        this.timer = null;

    };

    componentDidMount() {
      this.timer = setInterval(() => this.setCurrent(), 1000);
     }

    componentWillUnmount() {
      if (this.timer != null){
        clearInterval(this.timer);
       }
     }


    setCurrent() {
      /* Load and set the currently activate track  */
        const set_current = (response) => {
          if (this.state.track !== response.track) {
            this.setState({track: response.track});
            this.setPlaylist()
          }
        };
        queued_fetch(this.state.api_url + "zenplaylist/get_current_info",
                     set_current)
    }

    setPlaylist() {
      /* Load and set the current playlist  */
        const set_state = (response) => {
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
                <li className={ item.text.includes(this.state.track) ? "active-track": "" } key={index} >{item.text}</li>
          ))}
        </div>
      );
    }
  }
