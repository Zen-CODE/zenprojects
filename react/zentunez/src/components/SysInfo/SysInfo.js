import React, { Component } from 'react';


export class SysInfo extends Component {
  /* This component contains the content of the settings popul. It
     also handles the saving on these settings
  */
  constructor(props){
    super(props);
    this.state = { store: props.store,
                   show_sys_info: props.store.show_sys_info };
    this.unsubscribe = props.store.subscribe(() => this.storeChanged(props.store));
  }

  storeChanged(store) {
    // React to changes in the shared stated
    console.log("SysInfo. setting changed to " + store.getState().show_sys_info)
    this.setState({ show_sys_info: store.getState().show_sys_info });
  }

  render() {
    // We only return the component if enabled
    if ( this.state.show_sys_info) {
        return (
            <div>Sysinfo Dude! </div>)
    } else {
        return null
    };
  }
}
