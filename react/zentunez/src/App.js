import React, { Component } from 'react';
import './App.css';



function PlayerButton(props) {
  return (
    <button
      className="player"
      onClick={() => props.onClick()}
    >
      {props.caption}
    </button>
  );
}


class App extends Component {

  renderButton(caption) {
    return <PlayerButton
              caption={caption} 
            />;
  }

  render() {
    return (
      <div className="App">
        <div className="Player-Buttons">
          {this.renderButton("Previous")}
          {this.renderButton("Stop")}          
          {this.renderButton("Play / Pause")}
          {this.renderButton("Next")}
        </div>
      </div>
    );
  }
}

export default App;
