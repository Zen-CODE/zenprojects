import React, { Component } from 'react';
import './App.css';



function PlayerButton(props) {
  return (
    <button
      className="PlayerButton"
      onClick={() => props.onClick()}
    >
      {props.caption}
    </button>
  );
}

function Divider(props) {
  return (<div className="Divider" ></div>);
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
        <div className="PlayerButtons">
          {this.renderButton("Previous")}
          {Divider()}
          {this.renderButton("Stop")}          
          {Divider()}
          {this.renderButton("Play / Pause")}
          {Divider()}
          {this.renderButton("Next")}
        </div>
      </div>
    );
  }
}

export default App;
