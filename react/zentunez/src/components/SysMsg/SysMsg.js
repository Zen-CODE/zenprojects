
import React, { Component } from 'react';

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
    this.messages = [];
  }

  storeChanged(store) {
    // React to the sending of messages. Place them in the queue and activate the
    // timer.
    const msg = store.getState().show_sys_msg;
    this.messages.unshift(msg);
    this.setTimer(true);
  }

  timerEvent(event) {
    // The timer event has been fired. If there are messages to display. show
    // them, otherwise remove the notification display
    if (this.messages.length > 0) {
      this.setState({ msg: this.messages.pop() })
    } else {
      this.setState({ msg: "" })
      this.setTimer(false)
    }
  }

  setTimer(on) {
      // Switch the Timer on to start showing the message
      if (on && (this.intervalID === null)) {
        this.setState({ msg: this.messages.pop()});
        this.intervalID = setInterval(this.timerEvent.bind(this), 2000);
      } else if (!on && (this.intervalID != null)) {
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
    if ( this.state.msg != "" ) {
        return (
            <div className="message-area" >{ this.state.msg }</div>)
    } else {
        return null
    };
  }
}
