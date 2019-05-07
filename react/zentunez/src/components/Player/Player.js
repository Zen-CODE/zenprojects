import React, { Component } from 'react';
import { HDivider, VDivider } from '../Divider/Divider.js'
import { PlayerButton } from "../PlayerButton/PlayerButton.js"
import { PlayerState } from "../PlayerState/PlayerState.js"
import { VolumeSlider } from "../VolumeSlider/VolumeSlider.js"
import { Column, Row } from 'simple-flexbox';

export class Player extends Component {
    /*
    This class houses functionality to control the currently playting MPRIS2
    audio player and retreive state information from it.
    */
   constructor(props) {
      super(props);
      this.api_url = "http://127.0.0.1:8000/";
      /* The API that supplies the Media player functions */
  
      this.state = {artist: "-",
                    album: "-",
                    track: "-",
                    volume: 0,
                    state: "-",
                    position: 0,
                    img_src: ""};
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
      fetch(this.api_url + api_call)
        .then(res => res.json())
        .then((response) => {
            console.log("Volume is " + response.volume + ". Playing " + response.track);
            this.setState({artist: response.artist,
                          album: response.album,
                          track: response.track,
                          volume: response.volume,
                          state: response.state,
                          position: response.position,
                          img_src : this.api_url + "player/cover?guid=" + response.artist + response.album + response.track
                          })
        }
      )
    }
  
    setVolumne = (vol) => {
      fetch(this.api_url + "player/volume_set/" + (vol.target.valueAsNumber / 100.0))
      this.Click("player/state")
    }
  
    renderButton(caption, api_call) {
      return <PlayerButton
                caption={caption} 
                callback={this.Click}
                api_call={api_call}
              />;
    }
  
    renderVolume() {
      return <VolumeSlider 
                volume={ this.state.volume }
                onChange={ this.setVolumne }
             />
    }
  
    renderState() {
      return <PlayerState 
        artist={ this.state.artist } 
        track={ this.state.track }
        album={ this.state.album }
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
        <div>
          <Row horizontal='center'>
            <Column>{this.renderButton("Previous", "player/previous")}</Column>
            <HDivider />
            <Column>{this.renderButton("Stop", "player/stop")}</Column>
            <HDivider />
            <Column>{this.renderButton("Play / Pause", "player/play_pause")}</Column>
            <HDivider />
            <Column>{this.renderButton("Next", "player/next")}</Column>
          </Row>
          <VDivider />
          <Row horizontal='center' >
            <Column>{this.renderButton("<<", "player/volume_down")}</Column>
            <HDivider />
            <Column>            
              { this.renderVolume() }
            </Column>
            <HDivider />
            <Column>{this.renderButton(">>", "player/volume_up")}</Column>
          </Row>
          <Row horizontal='center'>
            {this.renderState()}
          </Row>
        </div>
      );
    }
  }
  