import React, { Component } from 'react';
import { MDBRow, MDBCol, MDBIcon } from "mdbreact";


class SettingsContent extends Component {
  /* This component contains the content of the settings popul. It
     also handles the saving on these settings
  */
  constructor(props){
    super(props);
    var state = props.store.getState();
    this.state = { store: props.store,
                   api_url: state.api_url,
                   auto_add: state.auto_add,
                   show_sys_info: false };
    this.unsubscribe = props.store.subscribe(() => this.storeChanged(props.store));
  }

  storeChanged(store) {
    // React to changes in the shared stated
    var state = store.getState();
    this.setState({ api_url: state.api_url,
                    auto_add: state.auto_add});
    }

  showSysyemInfoChanged (event) {
    // Toggle the state of the "Show System Information" setting
    var now = Date.now();
    var new_val = "New message " + now.toString();
    console.log("Sending message: " + new_val)
    this.setState({ show_sys_info: new_val })
    this.state.store.dispatch({
      type: "SHOW_SYS_MSG",
      show_sys_msg: new_val })
  }

  autoAddChanged (event) {
    // Toggle the state of the "Automatically add on last track"
    const new_val = !this.state.auto_add;
    this.setState({ auto_add: new_val })
    this.state.store.dispatch({
      type: "AUTO_ADD_CHANGED",
      auto_add: new_val })
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
          <MDBCol>Show System Msg</MDBCol>
          <MDBCol>
            <input type="checkbox"
                onChange={ (event) => this.showSysyemInfoChanged(event) }
            />
          </MDBCol>
        </MDBRow>
        <MDBRow>
          <MDBCol>Automatically play when stopped</MDBCol>
          <MDBCol>
            <input type="checkbox" checked={ this.state.auto_add }
                onChange={ (event) => this.autoAddChanged(event) }
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