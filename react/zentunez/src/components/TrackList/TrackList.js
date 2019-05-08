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
                    tracks: []
        }
    };

    componentDidUpdate(prevProps){
      // When the album changes, load the new track listing
      if ((this.props.album !== prevProps.album) || (this.props.artist !== prevProps.artist)) {
        this.setState({
          artist: this.props.artist,
          album: this.props.album,
          api_url: this.props.api_url,
        })
        this.setTracks(this.props.artist, this.props.album)
      }
    }

    setTracks(artist, album) {
      /* Set the Track listing to the current album */
      console.log("setAlbum() called with " + artist + ": " + album)
      fetch(this.state.api_url + "library/tracks/" + escape(artist) + "/" + escape(album))
      .then(res => res.json())
      .then((response) => {
          console.log("got response " + response)
          this.setState({tracks: response})
        }
      )
    }
  

    render(){
      return (
        <div className="track-list no-bullet" >
          <p><b>{ this.state.artist }:</b> { this.state.album }</p>
            { this.state.tracks.map((item, index) => (
                <li key={index}>{item}</li>
            ))}
        </div>
      );
    }
  }