import React, { Component } from 'react';
import { Player } from "./components/Player/Player.js"
import './App.css';


class App extends Component {
  /*
    The main application class for the ZenTunez React Interface
  */

  render(){
    return <div className="App">
      <Player />
    </div> 

  }
}

export default App;
