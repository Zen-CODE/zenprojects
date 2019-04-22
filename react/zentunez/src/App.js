import React, { Component } from 'react';
import './App.css';



function PlayerButton(props) {
  return (
    <button
      className="PlayerButton"
      onClick={() => props.callback()}
    >
      {props.caption}
    </button>
  );
}

function Divider(props) {
  return (<div className="Divider" ></div>);
}


class App extends Component {

  renderButton(caption, callback) {
    return <PlayerButton
              caption={caption} 
              callback={callback}
            />;
  }

  playerClick(){
    console.log("Tuzez Text!")
  }

  render() {
    return (
      <div className="App">
        <div className="PlayerButtons">
          {this.renderButton("Previous", this.playerClick)}
          {Divider()}
          {this.renderButton("Stop", this.playerClick)}          
          {Divider()}
          {this.renderButton("Play / Pause", this.playerClick)}
          {Divider()}
          {this.renderButton("Next", this.playerClick)}
        </div>
      </div>
    );
  }
}

export default App;
