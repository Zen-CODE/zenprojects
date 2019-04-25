import React, { Component } from 'react';
import { Divider } from './components/Divider/Divider.js'
import { PlayerImage } from "./components/PlayerImage/PlayerImage.js"
import { PlayerButton } from "./components/PlayerButton/PlayerButton.js"
import { PlayerState } from "./components/PlayerState/PlayerState.js"
import './App.css';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {artist: "-",
                  album: "-",
                  track: "-",
                  volume: 0,
                  state: "-",
                  position: 0,
                  img_src: ""};
    this.playerClick("player/state");
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
    const url = "http://127.0.0.1:5000/tunez/api/v1.0/"

    fetch(url + api_call)
      .then(res => res.json())
      .then((response) => {
          this.setState({artist: response.artist,
                         album: response.album,
                         track: response.track,
                         volume: response.volume,
                         state: response.state,
                         position: response.position,
                         img_src : url + "player/cover?guid=" + response.artist + response.album + response.track
                        })})          
  }

  render() {
    /** 
     * The main application objects are build and returned here.
    */
    return (
      <div className="App">
        <div className="PlayerButtons">
          {this.renderButton("Previous", "player/previous")}
          <Divider />
          {this.renderButton("Stop", "player/stop")}          
          <Divider />
          {this.renderButton("Play / Pause", "player/play_pause")}
          <Divider />
          {this.renderButton("Next", "player/next")}
        </div>
        <div className="PlayerButtons">
          {this.renderButton("Volume down", "player/volume_down")}          
          <Divider />
          {this.renderButton("Volume up", "player/volume_up")}
        </div>
        <div className="PlayerButtons">
          <PlayerState 
            artist={ this.state.artist } 
            album={ this.state.album }
            track={ this.state.track }
            volume={ this.state.volume }
            position={ this.state.position }
            state={ this.state.state }
            img_src={ this.state.img_src }
            />
        </div>
        <div className="PlayerButtons">
          <PlayerImage />
        </div>
      </div>
    );
  }
}

export default App;
