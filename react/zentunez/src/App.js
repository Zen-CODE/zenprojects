import React, { Component } from 'react';
import { Divider } from './components/Divider/Divider.js'
import {PlayerImage} from "./components/PlayerImage/PlayerImage.js"
import './App.css';




function PlayerButton(props) {
  return (
    <button
      className="PlayerButton"
      api_call={props.api_call}
      onClick={() => props.callback(props.api_call)}
    >
      {props.caption}
    </button>
  );
}

class App extends Component {

  renderButton(caption, api_call) {
    return <PlayerButton
              caption={caption} 
              callback={this.playerClick}
              api_call={api_call}
            />;
  }

  playerClick(api_call){
    /* Handle the click on a Player media button */
    console.log("Tuzez Text! " + api_call)
    const url = "http://127.0.0.1:5000/tunez/api/v1.0/"

    fetch(url + api_call)
      .then(function(response) {
        if (response.status === 200){
          console.log("Successful response")}
        else {
          console.log("Got reponse " + response.status + ", " + response.statusText)}
      })
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
          <PlayerImage />
        </div>
      </div>
    );
  }
}

export default App;
