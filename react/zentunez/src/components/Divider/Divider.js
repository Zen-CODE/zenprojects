import React, { Component } from 'react';
import './Divider.css';


export class VDivider extends Component {
  /**
   * A convenience class for separating the buttons vertically independently of styling
   */
    render(){
        return (<div className="v-divider" ></div>);
    }
}

export class HDivider extends Component {
    /**
     * A convenience class for separating the buttons horizontally independently of styling
     */
      render(){
          return (<div className="h-divider" ></div>);
      }
  }