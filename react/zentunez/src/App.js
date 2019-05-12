import React, { Component } from 'react';
import { Player } from "./components/Player/Player.js"
import { Library } from "./components/Library/Library.js"
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
    return <MDBContainer className="App" max-width="100%">
      <MDBRow>
        <MDBCol><Library api_url={ API_URL } /></MDBCol>
        <MDBCol size="0.5" ><Player api_url={ API_URL } /></MDBCol>
        <MDBCol><Library api_url={ API_URL } /></MDBCol>
      </MDBRow>
    </MDBContainer> 

  }
}

export default App;
