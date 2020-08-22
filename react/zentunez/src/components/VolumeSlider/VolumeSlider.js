import React, { Component } from 'react';

export class VolumeSlider extends Component {
    /**
     * This component displays the volume slider
     */    
    constructor(props) {
        super(props);
        this.state = {volume: 0.5}
      };

    render(){
      return (
          <input type="range" min="0" max="100" value={ 100 * this.props.volume } className="custom-range" onChange={ this.props.onChange } />
      );
    }
  }