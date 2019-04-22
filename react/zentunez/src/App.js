import React, { Component } from 'react';
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

function Divider(props) {
  /**
   * A convenience class for separating the buttons independently of styling
   */
  return (<div className="Divider" ></div>);
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
        console.log("Got response " + response)  
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
          {Divider()}
          {this.renderButton("Stop", "player/stop")}          
          {Divider()}
          {this.renderButton("Play / Pause", "player/play_pause")}
          {Divider()}
          {this.renderButton("Next", "player/next")}
        </div>
      </div>
    );
  }
}

export default App;
