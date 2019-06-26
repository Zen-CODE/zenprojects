import React, { Component } from 'react';
import { VDivider } from '../Divider/Divider.js'
import { TrackList } from "../TrackList/TrackList.js"
import { MDBContainer, MDBRow, MDBCol, MDBIcon } from "mdbreact";
import ReactTooltip from 'react-tooltip'

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
          store: props.store,
          auto_add: props.auto_add,
          timer: false
        }
        this.getRandomAlbum();
        this.unsubscribe = props.store.subscribe(() => this.storeChanged(props.store));
        this.timer = false;
      };

      storeChanged(store) {
        // React to changes in the shared stated
        var state = store.getState();
        this.setState({ api_url: state.api_url,
                        auto_add: state.auto_add
         });
         console.log("Auto_add = " + state.auto_add.toString())
      }

    lastTrack() {
      // The last track has been plated. Automatically add if appropriate
      console.log("The lastg track is playing...");
    }

    getAlbum() {
      /*
      Retrieve a random albom or search for a match if a search criteria has
      been entered.
      */
      if (this.state.search === ""){
        this.getRandomAlbum() }
      else {
        this.getSearchAlbum(this.state.search)}
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
          this.getSearchAlbum(this.state.search) }
        else {
          // this.showPopup("Invalid Search Term", "Please enter a valid search tem.")}
          this.getRandomAlbum()}
      }
    }

    onImageClick = () => {
      /* When the image is clicked, open the cover in a new window */
      window.open(this.state.api_url + "library/cover/" + this.state.artist + "/" + this.state.album)
    }

    renderIcon(icon, tooltip, callback) {
      // Render the specified MDBIcon and call the *callback* when clicked
      return <MDBIcon
                className="far"
                icon={ icon }
                data-tip={ tooltip }
                onClick={ () => callback() }>
                </MDBIcon>
    }

    timerEvent() {
      /// Fire the timer event
      this.getAlbum();
    }

    toggleTimer(){
      // Switch the timer for selecting random albums on and off
      this.setState({ timer: !this.state.timer });
      if (!this.state.timer) {
        this.timerEvent();
        this.timer = setInterval(() => this.timerEvent(), 10000);
      } else {
        if (this.timer != null){
          clearInterval(this.timer);
         }
      }
    }

    render(){
      return (
        <div>
          <ReactTooltip />
          <p><b>ZenTunez Library</b></p>
          <MDBContainer>
            <MDBRow>
              <MDBCol>{ this.renderIcon("search", "Choose a random album", this.getAlbum.bind(this))}</MDBCol>
              <MDBCol>
              <input
                data-tip="Enter a search term"
                onChange={(event) => this.searchChanged(event) }
                onKeyDown={ this.onKeyDown }>
              </input>
              </MDBCol>
              <MDBCol>{ this.renderIcon("sign-in-alt", "Enqueue this album", this.enqueueAlbum.bind(this)) }</MDBCol>
              <MDBCol>{ this.renderIcon("play", "Play this album", this.playAlbum.bind(this)) }</MDBCol>
              <MDBCol>{ this.renderIcon( this.state.timer ? "calendar-times": "clock"  , "Toggle to timer on and off", this.toggleTimer.bind(this)) }</MDBCol>
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
            last_track_cb={this.lastTrack }
          />
        </div>
      );
    }
  }