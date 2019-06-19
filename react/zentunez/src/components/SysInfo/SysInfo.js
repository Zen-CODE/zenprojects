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
    this.intervalID = null;
    if (props.store.show_sys_info) { this.setTimer(true) }
  }

  storeChanged(store) {
    // React to changes in the shared stated
    const si = store.getState().show_sys_info;
    console.log("SysInfo. setting changed to " + si)
    this.setState({ show_sys_info: si });
    this.setTimer(si);
  }

  timerEvent(event) {
    // The timer event has been fired
    console.log("Timer fired.")
  }

  setTimer(on) {
      // Switch the Timer on and off
      if (on && (this.intervalID === null)){
        console.log("Starting timer");
        this.intervalID = setInterval(this.timerEvent);
      } else if (!on && (this.intervalID != null)){
        console.log("Killing timer");
        clearInterval(this.intervalID);
        this.intervalID = null
      }
  }

  componentDidMount() {
    // When our component loads, switch the timer on if the setting demands it
    if (( this.intervalID === null) && (this.state.show_sys_info)) {
        this.setTimer(true);
    }
  }

  componentWillUnmount() {
    // When out component unloads, destory the timer if it's running
    if ( this.intervalID != null) {
        this.setTimer(false);
    }
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
