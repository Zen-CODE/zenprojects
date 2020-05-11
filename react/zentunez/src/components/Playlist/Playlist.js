import React, { Component } from 'react';
import '../TrackList/TrackList.css';
import { queued_fetch } from "../../functions/network.js"


export class Playlist extends Component {
    /**
     * This component handles the display of the track list for an album
     */
    constructor(props) {
        super(props);
        var state = props.store.getState();
        this.state = {
                    api_url: state.api_url,
                    tracks: [],
                    track: ""};
        this.unsubscribe = props.store.subscribe(() => this.storeChanged(props.store));
    };

    storeChanged(store) {
      // React to changes in the shared stated
      var state = store.getState();
      this.setState({ api_url: state.api_url,
                      track: state.track });
      this.setCurrent();
    }

    componentWillUnmount() {
       this.unsubscribe();
    }


    setCurrent() {
      /* Load and set the currently activate track  */
      const set_current = (response) => {
          this.setPlaylist()
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
