import React, { Component } from 'react';
import { HDivider, VDivider } from '../Divider/Divider.js'
import { PlayerButton } from "../PlayerButton/PlayerButton.js"
import { PlayerState } from "../PlayerState/PlayerState.js"
import { VolumeSlider } from "../VolumeSlider/VolumeSlider.js"
import { TrackList } from "../TrackList/TrackList.js"
import { MDBContainer, MDBRow, MDBCol } from "mdbreact";


export class Player extends Component {
    /*
    This class houses functionality to control the currently playting MPRIS2
    audio player and retreive state information from it.
    */
   constructor(props) {
      super(props);  
      this.state = {artist: "-",
                    album: "-",
                    track: "-",
                    volume: 0,
                    state: "-",
                    position: 0,
                    img_src: "",
                    api_url: props.api_url
                  };
      this.intervalID = 0;
    };
  
    componentDidMount(){
      this.intervalID = setInterval(() => this.Click("player/state"), 1000);
    }
  
    componentWillUnmount() {
      clearInterval(this.intervalID);
    }
  
    Click = (api_call) => {
      /* Handle the click on a Player media button */
      fetch(this.state.api_url + api_call)
        .then(res => res.json())
        .then((response) => {
            this.setState({artist: response.artist,
                          album: response.album,
                          track: response.track,
                          volume: response.volume,
                          state: response.state,
                          position: response.position,
                          img_src : this.state.api_url + "player/cover?guid=" + response.artist + response.album + response.track
                          })
        }
      )
    }

    setVolume = (vol) => {
      fetch(this.state.api_url + "player/volume_set/" + (vol.target.valueAsNumber / 100.0))
      this.Click("player/state")
    }
  
    renderButton(caption, api_call) {
      return <PlayerButton
                caption={caption} 
                onClick={ () => this.Click(api_call) }
              />;
    }
  
    renderVolume() {
      return <VolumeSlider 
                volume={ this.state.volume }
                onChange={ this.setVolume }
             />
    }

    renderTrackList(){
      return <TrackList 
                artist={ this.state.artist }
                album={ this.state.album }
                api_url={ this.state.api_url }
      />
    }
  
    renderState() {
      return <PlayerState 
        track={ this.state.track }
        position={ this.state.position }
        state={ this.state.state }
        img_src={ this.state.img_src }
      />
    }
  
    render() {
      /** 
       * The main application objects are build and returned here.
      */
      return (
        <MDBContainer>
          <MDBRow horizontal='center'>
            <MDBCol>{this.renderButton("Previous", "player/previous")}</MDBCol>
            <MDBCol>{this.renderButton("Stop", "player/stop")}</MDBCol>
            <MDBCol>{this.renderButton("Play / Pause", "player/play_pause")}</MDBCol>
            <MDBCol>{this.renderButton("Next", "player/next")}</MDBCol>
          </MDBRow>
          <VDivider />
          <MDBRow horizontal='center' >
            <MDBCol size="3">{this.renderButton("<<", "player/volume_down")}</MDBCol>
            <MDBCol>{ this.renderVolume() }</MDBCol>
            <MDBCol size="3">{this.renderButton(">>", "player/volume_up")}</MDBCol>
          </MDBRow>
          <MDBRow horizontal='center'>
            { this.renderState() }
          </MDBRow>
          <MDBRow>
            { this.renderTrackList() }
          </MDBRow>
        </MDBContainer>
      );
    }
  }
  