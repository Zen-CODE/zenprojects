import React, { Component } from 'react';
import { Player } from "./components/Player/Player.js"
import { Library } from "./components/Library/Library.js"
import { SettingsIcon } from "./components/Settings/SettingsIcon.js"
import '@fortawesome/fontawesome-free/css/all.min.css';
import 'bootstrap-css-only/css/bootstrap.min.css';
import 'mdbreact/dist/css/mdb.css';
import { MDBContainer, MDBRow, MDBCol } from "mdbreact";
import './App.css';
import { Popup } from "./components/Popup/Popup.js"


const API_URL = "http://10.0.0.3:8000/";

class App extends Component {
  /*
    The main application class for the ZenTunez React Interface
  */
  constructor(props) {
    super(props);
    this.popup = React.createRef();
  }

  render(){
    return <div>
      <Popup ref={ this.popup }/>
      <SettingsIcon username="Bob" popup={ this.popup } api_url={ API_URL } />
      <MDBContainer className="App">
        <MDBRow>
          <MDBCol><Library api_url={ API_URL } popup={ this.popup } /></MDBCol>
          <MDBCol><Player api_url={ API_URL } /></MDBCol>
          <MDBCol><Library api_url={ API_URL } popup={ this.popup }  /></MDBCol>
        </MDBRow>
      </MDBContainer> 
    </div>
  }
}

export default App;
