import React, { Component } from 'react';
import { VDivider } from '../Divider/Divider.js'
import { TrackList } from "../TrackList/TrackList.js"
import { MDBContainer, MDBRow, MDBCol, MDBIcon } from "mdbreact";
import { queued_fetch } from "../../functions/network.js"
import { send_message } from "../SysMsg/SysMsg.js"
// import { MDBSelect, MDBSelectInput, MDBSelectOptions, MDBSelectOption } from "mdbreact";

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
          path: "-",
          img_src: "",
          search: "",
          api_url: props.store.getState().api_url,
          store: props.store,
          mode: "add",
          timer: false
        }
        this.getRandomAlbum();
        this.unsubscribe = props.store.subscribe(() => this.storeChanged(props.store));
        this.timer = false;
      };

      storeChanged(store) {
        // React to changes in the shared stated
        var state = store.getState();
        this.setState({ api_url: state.api_url });
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
      send_message(this.state.store, "Getting random album...", "command");
      const set_state = (response) => {
        this.setState({
          artist: response.artist,
          album: response.album,
          path: response.path,
          img_src : this.state.api_url + `zenlibrary/get_album_cover?artist=${encodeURIComponent(response.artist)}&album=${encodeURIComponent(response.album)}`
          })

      };

      queued_fetch(this.state.api_url + "zenlibrary/get_random_album", set_state, true)
    }

    getSearchAlbum(term) {
      /* Handle the click to search for an album */
      send_message(this.state.store, "Searching for album...", "command");
      const set_state = (response) => {
        if ("artist" in response){
          this.setState({artist: response.artist,
                        album: response.album,
                        path: response.path,
                        img_src : this.state.api_url + `zenlibrary/get_album_cover?artist=${encodeURIComponent(response.artist)}&album=${encodeURIComponent(response.album)}`
                        })}
        else {
          this.showPopup("No matches",
          "No album found matching the search term (" + term + ")")
        }
      };

      queued_fetch(this.state.api_url + `zenlibrary/search?query=${encodeURIComponent(term)}`, set_state, true);
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


    playAlbum() {
      /* Add the current album to the queue in the currently playing audio player
      */
      send_message(this.state.store, "Playing album...", "command");
      queued_fetch(this.state.api_url + `zenplaylist/add_files?folder=${encodeURIComponent(this.state.path)}&mode=${this.state.mode}`, null, true);
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
          this.getRandomAlbum()}
      }
    }

    onImageClick = () => {
      /* When the image is clicked, open the cover in a new window */
      window.open(this.state.api_url + `zenlibrary/get_album_cover?artist=${encodeURIComponent(this.state.artist)}&album=${encodeURIComponent(this.state.album)}`)
    }

    renderIcon(icon, callback) {
      // Render the specified MDBIcon and call the *callback* when clicked
      return <MDBIcon
                className="far"
                icon={ icon }
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

    renderModeDropdown() {
      return (<div>
        <select className="browser-default custom-select"
          onChange={(event) => this.setMode(event) }
        >
          <option value="add">Add</option>
          <option value="next">Next</option>
          <option value="insert">Insert</option>
          <option value="replace">Replace</option>
        </select>
        </div>)
    };

    setMode(event) {
      this.setState({ 'mode': event.target.value })
    }

    render(){

        var back_style = {
          backgroundImage: 'url("' + encodeURI(this.state.img_src) + '")',
        };

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
              <MDBCol>{ this.renderModeDropdown() } </MDBCol>
              <MDBCol>{ this.renderIcon("play", this.playAlbum.bind(this)) }</MDBCol>
              <MDBCol>{ this.renderIcon( this.state.timer ? "calendar-times": "clock"  , this.toggleTimer.bind(this)) }</MDBCol>
            </MDBRow>
          </MDBContainer>
          <VDivider />
          <div>
            <div className="album-cover" alt="Album cover" style={ back_style } onClick={ this.onImageClick }></div>
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