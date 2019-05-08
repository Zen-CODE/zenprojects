import React, { Component } from 'react';
import './Library.css';
import { VDivider } from '../Divider/Divider.js'
import { TrackList } from "../TrackList/TrackList.js"

export class Library extends Component {
    /**
     * This component displays the volume slider
     */    
    constructor(props) {
        super(props);
        this.state = {
          artist: "-",
          album: "-",
          img_src: "",
          api_url: props.api_url
        }
        this.getRandomAlbum();
      };  

    getRandomAlbum() {
      /* Handle the click to fetdch a new randwom alum */
      fetch(this.state.api_url + "library/random_album")
        .then(res => res.json())
        .then((response) => {
            console.log("Random album is" + response.artist + " - " + response.album);
            this.setState({artist: response.artist,
                          album: response.album,
                          img_src : this.state.api_url + "library/cover/" + response.artist + "/" + response.album
                          })
        }
      )
    }

    enqueueAlbum() {
      /* Add the current album to the queue in the currently playing audio player    
      */
      fetch(this.state.api_url + `library/folder_enqueue/` + this.state.artist + "/" + this.state.album)
        .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
        .catch(error => console.error(error));
    }

    playAlbum() {
      /* Add the current album to the queue in the currently playing audio player    
      */
      fetch(this.state.api_url + `library/folder_play/` + this.state.artist + "/" + this.state.album)
        .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
        .catch(error => console.error(error));
    }

    render(){
      return (
        <div className="library-panel">
          <p><b>ZenTunez Library</b></p>
          <div>
            <button onClick={() => this.getRandomAlbum()}>Random album</button>
            <button onClick={() => this.enqueueAlbum()}>Enqueue </button>
            <button onClick={() => this.playAlbum()}>Play</button>
          </div>
          <VDivider />
          <div>
            <img className="album-cover" alt="Album cover" src={ this.state.img_src }></img>
          </div>
          <VDivider />
          <TrackList
            artist={ this.state.artist }
            album={ this.state.album } 
            api_url={ this.state.api_url }
          />
          <VDivider />
        </div>
      );
    }
  }