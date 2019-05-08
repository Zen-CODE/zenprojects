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
                    api_url: "",
                    tracks: []
        }
    };

    componentDidUpdate(prevProps, prevState){
      if (this.state.artist !== prevProps.artist){
        this.setState({
          artist: prevProps.artist,
          album: prevProps.album,
          api_url: prevProps.api_url,
        })
      this.setTracks(prevProps.artist, prevProps.album)
      }
    }

    setTracks(artist, album) {
      /* Set the Track listing to the current album */
      console.log("setAlbum() called with " + artist + ": " + album)
      console.log("api_url=" + this.state.api_url)
      fetch(this.state.api_url + "library/tracks/" + artist + "/" + album)
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