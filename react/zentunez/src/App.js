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
    console.log("Tuzez Text! " + api_call)
  }

  render() {
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
