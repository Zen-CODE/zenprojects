import React, { Component } from 'react';
import { Player } from "./components/Player/Player.js"
import { Library } from "./components/Library/Library.js"
import { Column, Row } from 'simple-flexbox';
import './App.css';

const API_URL = "http://127.0.0.1:8000/";

class App extends Component {
  /*
    The main application class for the ZenTunez React Interface
  */

  render(){
    return <div className="App">
      <Row>
        <Column><Player api_url={ API_URL } /></Column>
        <Column><Library /></Column>
      </Row>
    </div> 

  }
}

export default App;
