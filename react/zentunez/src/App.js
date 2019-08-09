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
import tunez_store from './store/TunezStore.js'
import { createStore } from 'redux'
import { SysMsg } from "./components/SysMsg/SysMsg.js"


var api_url = localStorage.getItem("api_url");
if (!api_url) { api_url = "http://" + window.location.hostname  + ":8000/"};
var auto_add = localStorage.getItem("auto_add");
if (auto_add === null) { auto_add = false} else { auto_add = (auto_add !== "false") };

class App extends Component {
  /*
    The main application class for the ZenTunez React Interface
  */
  constructor(props) {
    super(props);
    this.popup = React.createRef();
    this.store = createStore(tunez_store,
                             { api_url: api_url,
                               auto_add: auto_add,
                               popup: this.popup
                             })
}

  render(){
    return (
    <div>
      <Popup ref={ this.popup }/>
      <SettingsIcon store={ this.store } />
      <MDBContainer className="App">
        <MDBRow>
          <MDBCol><Player store={ this.store } /></MDBCol>
          <MDBCol><Library store={ this.store } /></MDBCol>
          <MDBCol><Library store={ this.store } /></MDBCol>
        </MDBRow>
      </MDBContainer>
      <SysMsg store={ this.store }/>
    </div>)
  }
}

export default App;
