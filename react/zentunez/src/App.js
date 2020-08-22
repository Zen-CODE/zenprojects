import React, { Component } from 'react';
import { Player } from "./components/Player/Player.js"
import { Playlist } from "./components/Playlist/Playlist.js"
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
import { HDivider } from "./components/Divider/Divider.js"


var api_url = localStorage.getItem("api_url");
if (!api_url) { api_url = "http://" + window.location.hostname  + ":" + window.location.port + "/"};

class App extends Component {
  /*
    The main application class for the ZenTunez React Interface
  */
  constructor(props) {
    super(props);
    this.popup = React.createRef();
    this.store = createStore(tunez_store,
                             { api_url: api_url,
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
          <HDivider />
          <MDBCol><Playlist store={ this.store } /></MDBCol>
          <HDivider />
          <MDBCol><Library store={ this.store } /></MDBCol>
        </MDBRow>
      </MDBContainer>
      <SysMsg store={ this.store }/>
    </div>)
  }
}

export default App;
