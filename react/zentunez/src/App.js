import React, { Component } from 'react';
import { Divider } from './components/Divider/Divider.js'
import { PlayerButton } from "./components/PlayerButton/PlayerButton.js"
import { PlayerState } from "./components/PlayerState/PlayerState.js"
import { VolumeSlider } from "./components/VolumeSlider/VolumeSlider.js"
import { Column, Row } from 'simple-flexbox';
import './App.css';


class App extends Component {
  /*
    The main application class for the ZenTunez React Interface
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
    
    setInterval(() => this.playerClick("player/state"), 1000);
  };

  renderButton(caption, api_call) {
    return <PlayerButton
              caption={caption} 
              callback={this.playerClick}
              api_call={api_call}
            />;
  }

  playerClick = (api_call) => {
    /* Handle the click on a Player media button */

    fetch(this.api_url + api_call)
      .then(res => res.json())
      .then((response) => {
          console.log("Volume is " + response.volume);
          this.setState({artist: response.artist,
                         album: response.album,
                         track: response.track,
                         volume: response.volume,
                         state: response.state,
                         position: response.position,
                         img_src : this.api_url + "player/cover?guid=" + response.artist + response.album + response.track
                        })})          
  }

  setVolumne = (vol) => {
    fetch(this.api_url + "player/volume_set/" + (vol.target.valueAsNumber / 100.0))
    this.playerClick("player/state")
  }

  render() {
    /** 
     * The main application objects are build and returned here.
    */
    return (
      <div className="App">
        <Row horizontal='center'>
          <Column>{this.renderButton("Previous", "player/previous")}</Column>
          <Divider />
          <Column>{this.renderButton("Stop", "player/stop")}</Column>
          <Divider />
          <Column>{this.renderButton("Play / Pause", "player/play_pause")}</Column>
          <Divider />
          <Column>{this.renderButton("Next", "player/next")}</Column>
        </Row>
        <Row horizontal='center' >
          <Column>{this.renderButton("<<", "player/volume_down")}</Column>
          <Divider />
          <Column>            
            <VolumeSlider 
              volume={ this.state.volume }
              onChange={ this.setVolumne }
            />
          </Column>
          <Divider />
          <Column>{this.renderButton(">>", "player/volume_up")}</Column>
        </Row>
        <Row horizontal='center'>
          <PlayerState 
            artist={ this.state.artist } 
            album={ this.state.album }
            track={ this.state.track }
            volume={ this.state.volume }
            position={ this.state.position }
            state={ this.state.state }
            img_src={ this.state.img_src }
            />
        </Row>
      </div>
    );
  }
}

export default App;
