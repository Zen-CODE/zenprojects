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
                    track: ""}
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
      return (
        <div className="track-list no-bullet" >
          {/* Header info */}
          { /*<li style={ divStyle }>&nbsp;</li> */}
          <div className="track-separator" />
          <b>{ this.state.artist }:</b> { this.state.album }
          <div className="track-separator" />

          {/* Track listing */}
          { this.state.tracks.map((item, index) => (
                <li className={ item === this.state.track ? "active-track": "" } key={index} >{item}</li>
          ))}
        </div>
      );
    }
  }
