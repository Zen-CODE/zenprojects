import React, { Component } from 'react';
import './TrackList.css';

export class TrackList extends Component {
    /**
     * This component handles the display of the track list for an album
     */
    constructor(props) {
      super(props);

      this.state = {artist: "-",
                    album: "-",
                    api_url: props.api_url,
                    tracks: [],
                    track: ""
        }
    };

    componentDidUpdate(prevProps){
      // When the album changes, load the new track listing
      if ((this.props.album !== prevProps.album) || (this.props.artist !== prevProps.artist)) {
        this.setState({
          artist: this.props.artist,
          album: this.props.album,
          api_url: this.props.api_url,
          track: this.props.track
        })
        this.setTracks(this.props.artist, this.props.album)
      } else if (this.props.track !== prevProps.track) {
        // If the current track has changed, update the listing so it's highlighted
        // this.setTracks(this.props.artist, this.props.album)
        this.setState({ track: this.props.track});
      }
    }

    setTracks(artist, album) {
      /* Set the Track listing to the current album */
      fetch(this.state.api_url + "library/tracks/" + artist + "/" + album)
      .then(res => res.json())
      .then((response) => {
          this.setState({tracks: response})
        }
      )
    }


    render(){
      const divStyle = {"height": "5px", "background-color": "#555555", "margin-top": "3px", "margin-bottom": "3px" };
      const len = (this.state.artist + this.state.album).length;

      return (
        <div className="track-list no-bullet" >
          {/* Header info */}
          { /*<li style={ divStyle }>&nbsp;</li> */}
          <div style={ divStyle } />
          <b>{ this.state.artist }:</b> { this.state.album }
          <div style={ divStyle } />

          {/* Track listing */}
          { this.state.tracks.map((item, index) => (
                <li className={ item === this.state.track ? "active-track": "" } key={index} >{item}</li>
          ))}
        </div>
      );
    }
  }