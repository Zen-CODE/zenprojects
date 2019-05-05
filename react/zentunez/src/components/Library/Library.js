import React, { Component } from 'react';
import './Library.css';
import { VDivider } from '../Divider/Divider.js'
import { postData } from '../../lib/post.js'

export class Library extends Component {
    /**
     * This component displays the volume slider
     */    
    constructor(props) {
        super(props);
        this.state = {
          artist: "-",
          album: "-",
          img_src: ""
        }
        this.api_url = "http://127.0.0.1:8000/";
        /* The API that supplies the Media library functions */
          
      };  

    getRandomAlbum() {
      /* Handle the click to fetdch a new randwom alum */
      fetch(this.api_url + "library/random_album")
        .then(res => res.json())
        .then((response) => {
            console.log("Random album is" + response.artist + " - " + response.album);
            this.setState({artist: response.artist,
                          album: response.album,
                          img_src : this.api_url + "library/cover/" + response.artist + "/" + response.album
                          })
        }
      )
    }

    enqueueAlbum() {
      /* Add the current album to the queue in the currently playing audio player    
      */
      fetch(this.api_url + `library/folder_enqueue/` + this.state.artist + "/" + this.state.album)
        .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
        .catch(error => console.error(error));
    }

    playAlbum() {
      /* Add the current album to the queue in the currently playing audio player    
      */
      fetch(this.api_url + `library/folder_play/` + this.state.artist + "/" + this.state.album)
        .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
        .catch(error => console.error(error));
    }

    render(){
      return (
        <div className="LibraryPanel">
          <p><b>ZenTunez Library</b></p>
          <VDivider />
          <p><b>Artist: </b>{ this.state.artist } </p>
          <p><b>Album: </b>{ this.state.album } </p>
          <VDivider />
          <img className="album-cover" alt="Album cover" src={ this.state.img_src }></img>
          <br />
          <VDivider />
          <button onClick={() => this.getRandomAlbum()}>Random album</button>
          <button onClick={() => this.enqueueAlbum()}>Enqueue </button>
          <button onClick={() => this.playAlbum()}>Play</button>
        </div>
      );
    }
  }