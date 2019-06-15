import React, { Component } from 'react';
import { MDBRow, MDBCol, MDBIcon } from "mdbreact";


class SettingsContent extends Component {
  /* This component contains the content of the settings popul. It
     also handles the saving on these settings
  */
  constructor(props){
    super(props);
    this.state = { store: props.store,
                   api_url: props.store.getState().api_url,
                   system_info: 'false' };
    this.unsubscribe = props.store.subscribe(() => this.storeChanged(props.store));
  }

  storeChanged(store) {
    // React to changes in the shared stated
    this.setState({ api_url: store.getState().api_url });
  }

  showSysyemInfoChanged (event) {
    // Toggle the state of the "Show System Information" setting
    this.setState({ system_info: this.state.system_info === 'false'? 'true': 'false' })
  }

  serverIPChanged (event) {
    // Dispatch the store change to the api_url
    const api_url = event.target.value;
    this.state.store.dispatch({
      type: "API_URL_CHANGED",
      api_url: api_url })
  }

  componentWillUnmount() {
    // When out component unloads, trhe binding to state changes
    this.unsubscribe()
  }

  render() {
    return (
      <MDBCol>
        <MDBRow>
          <MDBCol>Server IP:</MDBCol>
          <MDBCol>
            <input
                  onChange={ (event) => this.serverIPChanged(event) }
                  value={ this.state.api_url }>
            </input>
          </MDBCol>
        </MDBRow>
        <MDBRow>
          <MDBCol>Show System Info</MDBCol>
          <MDBCol>
            <input type="checkbox" checked={ this.state.system_info }
                onChange={ (event) => this.showSysyemInfoChanged(event) }
            />
          </MDBCol>
        </MDBRow>
      </MDBCol>
    )
  }
}

export class SettingsIcon extends Component {
    /**
     * This component displays the settings icon
     */
    constructor(props) {
        super(props);
        this.state = { store: props.store }
      };

    onClick()  {
        /* Respond to the clicking of the settings icon */
        const node = this.state.store.getState().popup.current;
        node.setState({ title: "Settings",
                        body: <SettingsContent store={ this.state.store }/>,
                        modal: true })
    }

    render(){
      return <div className="settings-icon">
                <MDBIcon
                  className="far"
                  icon="cogs"
                  onClick={ () => this.onClick() }
                  />
          </div>
    }
  }