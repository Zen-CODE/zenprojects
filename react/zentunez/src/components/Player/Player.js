import React, { Component } from 'react';
import { HDivider, VDivider } from '../Divider/Divider.js'
import { PlayerButton } from "../PlayerButton/PlayerButton.js"
import { PlayerState } from "../PlayerState/PlayerState.js"
import { VolumeSlider } from "../VolumeSlider/VolumeSlider.js"
import { TrackList } from "../TrackList/TrackList.js"
import { Column, Row } from 'simple-flexbox';

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
                callback={this.Click}
                api_call={api_call}
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
            { this.renderState() }
          </Row>
          <Row>
            { this.renderTrackList() }
          </Row>
        </div>
      );
    }
  }
  