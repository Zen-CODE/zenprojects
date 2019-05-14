import React, { Component } from 'react';
import { Player } from "./components/Player/Player.js"
import { Library } from "./components/Library/Library.js"
import { SettingsIcon } from "./components/Settings/SettingsIcon.js"
import '@fortawesome/fontawesome-free/css/all.min.css';
import 'bootstrap-css-only/css/bootstrap.min.css';
import 'mdbreact/dist/css/mdb.css';
import { MDBContainer, MDBRow, MDBCol } from "mdbreact";
import './App.css';

const API_URL = "http://127.0.0.1:8000/";

class App extends Component {
  /*
    The main application class for the ZenTunez React Interface
  */

  render(){
    return <div>
      <SettingsIcon />
      <MDBContainer className="App">
        <MDBRow>
          <MDBCol><Library api_url={ API_URL } /></MDBCol>
          <MDBCol><Player api_url={ API_URL } /></MDBCol>
          <MDBCol><Library api_url={ API_URL } /></MDBCol>
        </MDBRow>
      </MDBContainer> 
    </div>
  }
}

export default App;
