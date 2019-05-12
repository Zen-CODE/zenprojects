import React, { Component } from 'react';
import './Library.css';
import { VDivider, HDivider } from '../Divider/Divider.js'
import { TrackList } from "../TrackList/TrackList.js"
import { PlayerButton } from "../PlayerButton/PlayerButton.js"


export class Library extends Component {
    /**
     * This component selects random albums or searches for them, then present
     * them in the UI for either enqueueing or playing.
     */    
    constructor(props) {
        super(props);
        this.state = {
          artist: "-",
          album: "-",
          img_src: "",
          api_url: props.api_url,
          search: ""
        }
        this.getRandomAlbum();
      };  

    getAlbum() {
      /*
      Retrieve a random albom or search for a match if a search criteria has
      been entered.
      */
      if (this.state.search === ""){
        this.getRandomAlbum()
      } else {
        this.getSearchAlbum(this.state.search)
      }
    }

    getRandomAlbum() {
      /* Handle the click to fetch a new random album */
      fetch(this.state.api_url + "library/random_album")
        .then(res => res.json())
        .then((response) => {
            this.setState({artist: response.artist,
                          album: response.album,
                          img_src : this.state.api_url + "library/cover/" + response.artist + "/" + response.album
                          })
        }
      )
    }

    getSearchAlbum(term) {
      /* Handle the click to search for an album */
      fetch(this.state.api_url + "library/search/" + term)
        .then(res => res.json())
        .then((response) => {
            if ("artist" in response){
              this.setState({artist: response.artist,
                            album: response.album,
                            img_src : this.state.api_url + "library/cover/" + response.artist + "/" + response.album
                            })}
            else {
              alert("No album found matching the search term (" + term + ")")
            }
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

    searchChanged(event) {
      /* The search term has changed */
      this.setState({ 'search': event.target.value })
    }

    onKeyDown = (e) => {
      /* Catch the Enter keypress event to fire the search. */
      if (e.key === 'Enter') { this.getSearchAlbum(this.state.search) }
    }

    onImageClick = () => {
      /* When the image is clicked, open the cover in a new window */
      window.open(this.state.api_url + "library/cover/" + this.state.artist + "/" + this.state.album)
    }

    render(){
      return (
        <div className="library-panel">
          <p><b>ZenTunez Library</b></p>
          <div>
            <PlayerButton caption="Get album" onClick={ () => this.getAlbum() } />
            <HDivider />
            <input 
              onChange={(event) => this.searchChanged(event) }
              onKeyDown={ this.onKeyDown }>
            </input>
          </div>
          <VDivider />
          <div>
            <img className="album-cover" alt="Album cover" src={ this.state.img_src } onClick={ this.onImageClick }></img>
          </div>
          <VDivider />
          <TrackList
            artist={ this.state.artist }
            album={ this.state.album } 
            api_url={ this.state.api_url }
          />
          <VDivider />
          <div>
            <PlayerButton caption="Enqueue" onClick={() => this.enqueueAlbum()} />
            <HDivider />
            <PlayerButton caption="Play" onClick={() => this.playAlbum()} />
          </div>
        </div>
      );
    }
  }