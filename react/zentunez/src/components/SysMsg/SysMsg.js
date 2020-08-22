
import React, { Component } from 'react';

/**
 * The `send_message` function is a convenience function for sending messages for
 * the React frontend to display in the appriate place and at the appropriate
 * time.
 *
 * @param {Object} store - reference to the Redux store instance
 * @param {*} msg - the message to send
 * @param {*} msg_type - the type if message to send. Currently supported types
 *                       are "event" and "command"
 */
export function send_message(store, msg){
  console.log("SysMsg. Dispatching...")
  store.dispatch({
    type: "SHOW_SYS_MSG",
    msg: msg,
  })
}

/**
* @typedef {Object} SysMsg
* @property {Object} state - The object state as required by react
* @property {number} unsubscribe - The identifier of the subscription to store event
* @property {number} intervalID - The identifier of the timer interval event
* @property {string} msg - A strings containing the message currently displayed
* @property {boolean} reset - A strings containing the message currently displayed
* @property {Array} commands - A list of command messages in the notification queue
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
    this.msg = "";
    this.reset = false;
  }


   storeChanged(store) {
    // React to the sending of messages. Place them in the queue and activate the
    // timer.
    const state = store.getState();
    const msg = state.msg;

    if (msg) {
      this.msg = msg;
      this.setState({ msg: msg });
      this.reset = true}
    if (this.intervalID === null) { this.setTimer(true) };
  }

  timerEvent(event) {
    // The timer event has been fired. If there are messages to display, show
    // them, otherwise remove the notification display.
    if (this.reset) {
        this.reset = false
    } else {
      this.setState({ msg: "" });
      this.setTimer(false);
    }
  }

  setTimer(on) {
      // Switch the Timer on to start showing the message
      if (on && (this.intervalID === null)) {
        this.intervalID = setInterval(this.timerEvent.bind(this), 3000);
      } else if (!on && (this.intervalID != null)) {
        clearInterval(this.intervalID);
        this.intervalID = null;
        console.log("Stopping timer");
      }
  }

  componentDidMount() {
    // When our component loads, switch the timer on if the setting demands it
    if ( this.intervalID === null) {
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
