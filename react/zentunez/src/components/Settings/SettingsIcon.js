import React, { Component } from 'react';
import { MDBContainer, MDBRow, MDBCol, MDBIcon } from "mdbreact";
import tunez_store from '../../store/TunezStore.js'
import { createStore } from 'redux'


const store = createStore(tunez_store)

class SettingsContent extends Component {
  /* This component contains the content of the settings popul. It
     also handles the saving on these settings
  */
  constructor(props){
    super(props);
    this.state = { api_url: props.api_url }
  }

  serverIPChanged (event) {
    const api_url = event.target.value;
    console.log("Server ip = " + api_url );
    this.setState({ api_url: api_url });
    store.dispatch({
      type: "API_URL_CHANGED",
      api_url: api_url })
  }

  render() {
    return (
      <MDBRow>
        <MDBCol>Server IP:</MDBCol>
        <MDBCol>
          <input
                onChange={(event) => this.serverIPChanged(event) }
                value={ this.state.api_url }>
          </input>
        </MDBCol>
      </MDBRow>
    )
  }
}

export class SettingsIcon extends Component {
    /**
     * This component displays the settings icon
     */
    constructor(props) {
        super(props);
        this.state = {api_url: props.api_url,
                      username: props.username,
                      popup: props.popup
                     }
      };

    onClick()  {
        /* Respond to the clicking of the settings icon */
        const node = this.state.popup.current;
        node.setState({ title: "Settings",
                        body: <SettingsContent api_url={ this.state.api_url }/>,
                        modal: true })
    }

    render(){
      return <div className="settings-icon">
          <MDBContainer>
            <MDBRow>
              <MDBCol>
                <MDBIcon
                  className="far"
                  icon="cogs"
                  onClick={ () => this.onClick() }
                  />
                </MDBCol>
                <MDBCol>
                  <p>{ this.state.username }</p>
                </MDBCol>
              </MDBRow>
            </MDBContainer>
          </div>
    }
  }