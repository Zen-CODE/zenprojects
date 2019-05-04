import React, { Component } from 'react';
import './Library.css';
import { VDivider } from '../Divider/Divider.js'

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
                          //img_src : this.api_url + "player/cover?guid=" + response.artist + response.album
                          })
        }
      )
    }


    render(){
      return (
        <div className="LibraryPanel">
          <p><b>ZenTunez Library</b></p>
          <VDivider />
          <p><b>Artist:</b>{ this.artist } </p>
          <p><b>Album:</b>{ this.album } </p>
          <VDivider />
          <img className="album-cover" alt="Album cover" src={ this.props.img_src }></img>
          <br />
          <VDivider />
          <button onClick={() => this.getRandomAlbum()}>Random album</button>
        </div>
      );
    }
  }