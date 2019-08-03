
import React, { Component } from 'react';

// TODO: Add docs if this actually works
export function send_message(store, msg, msg_type ){
  console.log("SysMsg. Dispatching...")
  store.dispatch({
    type: "SHOW_SYS_MSG",
    msg: msg,
    msg_type: msg_type
  })
}

/**
* @typedef {Object} SysMsg
* @property {Object} state - The object state as required by react
* @property {number} unsubscribe - The identifier of the subscription to store event
* @property {number} intervalID - The identifier of the timer interval event
* @property {Array} messages - A list of messages in the notification queue
*/
export class SysMsg extends Component {
  /* This component contains the content of the settings popul. It
     also handles the saving on these settings
  */
  constructor(props){
    super(props);
    this.state = { store: props.store, msg: '' };
    this.unsubscribe = props.store.subscribe(() => this.storeChanged(props.store));
    this.intervalID = null;
    this.events = [];  // Log system events
    this.actions = [];  // Log system actions
  }

   storeChanged(store) {
    // React to the sending of messages. Place them in the queue and activate the
    // timer.
    const state = store.getState();
    const msg_type = state.msg_type;
    const msg = state.msg;

    console.log("Store change. msg: " + msg + ", msg_type: " + msg_type);
    // if (action) { this.actions.unshift("Executing " + action) };
    // if (msg) { this.messages.unshift(msg) };
    // if (this.intervalID === null && (msg || action)) { console.log("Starting timer"); this.setTimer(true) };
  }

  extractMessages() {
    // Extract the messages from the queue and generate the final message
    var msg = this.messages.length > 0 ? this.messages.pop(): "";
    msg = msg + this.actions.length > 0 ? " > " + this.actions.pop(): "";
    console.log("Extracting messages - " + msg);
    this.setState({ msg: msg });
    // this.state.store.dispatch({ type: "SHOW_SYS_MSG", show_sys_msg: "" });
    // this.state.store.dispatch({ type: "SHOW_SYS_ACTION", show_sys_action: "" });

  }

  timerEvent(event) {
    // The timer event has been fired. If there are messages to display. show
    // them, otherwise remove the notification display
    if (this.messages.length + this.actions.length > 0) {
      this.extractMessages();
    } else {
      this.setState({ msg: "" });
      this.setTimer(false);
    }
  }

  setTimer(on) {
      // Switch the Timer on to start showing the message
      if (on && (this.intervalID === null)) {
        this.intervalID = setInterval(this.timerEvent.bind(this), 3000);
        this.extractMessages();
      } else if (!on && (this.intervalID != null)) {
        clearInterval(this.intervalID);
        this.intervalID = null;
        console.log("Stopping timer");
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
    if ( this.state.msg !== "" ) {
        return (
            <div className="message-area" >{ this.state.msg }</div>)
    } else {
        return null
    };
  }
}
