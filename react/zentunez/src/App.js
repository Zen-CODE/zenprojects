import React, { Component } from 'react';
import { Player } from "./components/Player/Player.js"
import { Library } from "./components/Library/Library.js"
import { Column, Row } from 'simple-flexbox';
import './App.css';


class App extends Component {
  /*
    The main application class for the ZenTunez React Interface
  */

  render(){
    return <div className="App">
      <Row>
        <Column><Player /></Column>
        <Column><Library /></Column>
      </Row>
    </div> 

  }
}

export default App;
