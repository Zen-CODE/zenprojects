import React, { Component } from 'react';
import { queued_fetch } from "../../functions/network.js"
import { MDBContainer, MDBRow, MDBCol } from "mdbreact";

export class TrackMeta extends Component {
    /**
     * This component handles the display of the track list for an album
     */
    constructor(props) {
      super(props);

      this.state = {api_url: props.api_url,
                    track: "",
                    bitrate: "",
                    bitrate_mode: "",
                    channels: "",
                    sample_rate: ""}
    };

    componentDidUpdate(prevProps){
      // When the album changes, load the new track listing
      if ((this.props.track !== prevProps.track)) {
        this.setMeta();
      }
    }

    setMeta() {
      /* Set the Track listing to the current album */
        const set_state = (response) => { this.setState({
            bitrate: response.bitrate,
            bitrate_mode: response.bitrate_mode,
            channels: response.channels,
            sample_rate: response.sample_rate
        })};
        queued_fetch(this.state.api_url + `zenplayer/get_track_meta`, set_state)
    }

    render(){
      return (
        <MDBContainer>
          <div className="track-separator" />
          <MDBRow><MDBCol><b>Bitrate: { this.state.bitrate } kbps</b></MDBCol></MDBRow>
          <MDBRow><MDBCol><b>Mode: { this.state.bitrate_mode }</b></MDBCol></MDBRow>
          <MDBRow><MDBCol><b>Channels: { this.state.channels }</b></MDBCol></MDBRow>
          <MDBRow><MDBCol><b>Sample Rate: { this.state.sample_rate } hz</b></MDBCol></MDBRow>
        </MDBContainer>
      );
    }
  }

