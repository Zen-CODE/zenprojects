import React, { Component } from 'react';
import { queued_fetch } from "../../functions/network.js"
import { MDBContainer, MDBRow, MDBCol } from "mdbreact";

export class TrackMeta extends Component {
    /**
     * This component handles the display of the track list for an album
     */
    constructor(props) {
      super(props);

      this.state = {artist: "-",
                    album: "-",
                    api_url: props.api_url,
                    track: "",
                    bitrate: "",
                    bitrate_mode: "",
                    channels: "",
                    sample_rate: ""}
    };

    componentDidUpdate(prevProps){
      // When the album changes, load the new track listing
    //   if ((this.props.album !== prevProps.album) || (this.props.artist !== prevProps.artist)) {
    //     this.setState({
    //       artist: this.props.artist,
    //       album: this.props.album,
    //       api_url: this.props.api_url,
    //       track: this.props.track
    //     })
    //     this.setTracks(this.props.artist, this.props.album)
    //   } else if (this.props.track !== prevProps.track) {
    //     // If the current track has changed, update the listing so it's highlighted
    //     this.setState({ track: this.props.track});
    //   }
    }

    // setTracks(artist, album) {
    //   /* Set the Track listing to the current album */
    //   if (artist !== "" && album !== "") {
    //     const set_state = (response) => { this.setState({tracks: response}) };
    //     queued_fetch(this.state.api_url + `zenlibrary/get_tracks?artist=${encodeURIComponent(artist)}&album=${encodeURIComponent(album)}`,
    //                  set_state)
    //   }
    // }


    render(){
      return (
        <MDBContainer>
          <MDBRow><MDBCol><b>Bitrate: { this.state.bitrate }</b></MDBCol></MDBRow>
          <MDBRow><MDBCol><b>Mode: { this.state.bitrate_mode }</b></MDBCol></MDBRow>
          <MDBRow><MDBCol><b>Channels: { this.state.channels }</b></MDBCol></MDBRow>
          <MDBRow><MDBCol><b>Sample Rate: { this.state.sample_rate }</b></MDBCol></MDBRow>
        </MDBContainer>
      );
    }
  }
