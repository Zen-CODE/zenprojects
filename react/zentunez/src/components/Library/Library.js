import React, { Component } from 'react';
import { VDivider } from '../Divider/Divider.js'
import { TrackList } from "../TrackList/TrackList.js"
import { MDBContainer, MDBRow, MDBCol, MDBIcon } from "mdbreact";

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
          search: "",
          api_url: props.store.getState().api_url,
          store: props.store
        }
        this.getRandomAlbum();
        this.unsubscribe = props.store.subscribe(() => this.storeChanged(props.store));
      };

      storeChanged(store) {
        // React to changes in the shared stated
        this.setState({ api_url: store.getState().api_url });
      }

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
      const api_url = this.state.api_url;
      fetch(api_url + "library/random_album")
        .then(res => res.json())
        .then((response) => {
            this.setState({artist: response.artist,
                          album: response.album,
                          img_src : api_url + "library/cover/" + response.artist + "/" + response.album
                          })
        }
      )
    }

    getSearchAlbum(term) {
      /* Handle the click to search for an album */
      const api_url = this.state.api_url;
      fetch(api_url + "library/search/" + term)
        .then(res => res.json())
        .then((response) => {
            if ("artist" in response){
              this.setState({artist: response.artist,
                            album: response.album,
                            img_src : api_url + "library/cover/" + response.artist + "/" + response.album
                            })}
            else {
              this.showPopup("No matches",
              "No album found matching the search term (" + term + ")")
            }
        }
      )
    }

    showPopup(title, body){
      /**
       * Show a modal popup with the specified title and body.
       */
      const node = this.state.store.getState().popup.current;
      node.setState({ title: title,
                            body: body,
                            modal: true,
                          })
    }

    enqueueAlbum() {
      /* Add the current album to the queue in the currently playing audio player
      */
     const api_url = this.state.api_url;
      fetch(api_url + `library/folder_enqueue/` + this.state.artist + "/" + this.state.album)
        .catch(error => console.error(error));
    }

    playAlbum() {
      /* Add the current album to the queue in the currently playing audio player
      */
      const api_url = this.state.api_url;
      fetch(api_url + `library/folder_play/` + this.state.artist + "/" + this.state.album)
        .catch(error => console.error(error));
    }

    searchChanged(event) {
      /* The search term has changed */
      this.setState({ 'search': event.target.value })
    }

    onKeyDown = (e) => {
      /* Catch the Enter keypress event to fire the search. */
      if (e.key === 'Enter') {
        const len = this.state.search.length;
        if (len > 0) {
          this.getSearchAlbum(this.state.search)
        } else {
          this.showPopup("Invalid Search Term", "Please enter a valid search tem.")
        }
      }
    }

    onImageClick = () => {
      /* When the image is clicked, open the cover in a new window */
      window.open(this.state.api_url + "library/cover/" + this.state.artist + "/" + this.state.album)
    }

    renderIcon(icon, callback) {
      // Render the specified MDBIcon and call the *callback* when clicked
      return <MDBIcon
                className="far"
                icon={ icon }
                onClick={ () => callback() }
              />
    }

    render(){
      return (
        <div>
          <p><b>ZenTunez Library</b></p>
          <MDBContainer>
            <MDBRow>
              <MDBCol>{ this.renderIcon("search", this.getAlbum.bind(this))}</MDBCol>
              <MDBCol>
              <input
                onChange={(event) => this.searchChanged(event) }
                onKeyDown={ this.onKeyDown }>
              </input>
              </MDBCol>
              <MDBCol>{ this.renderIcon("sign-in-alt", this.enqueueAlbum.bind(this)) }</MDBCol>
              <MDBCol>{ this.renderIcon("play", this.playAlbum.bind(this)) }</MDBCol>
            </MDBRow>
          </MDBContainer>
          <VDivider />
          <div>
            <img className="album-cover" alt="Album cover" src={ this.state.img_src } onClick={ this.onImageClick }></img>
          </div>
          <TrackList
            artist={ this.state.artist }
            album={ this.state.album }
            api_url={ this.state.api_url }
          />
        </div>
      );
    }
  }