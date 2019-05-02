import React, { Component } from 'react';
import './VolumeSlider.css';

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
        <div className="volume-slider">
          <input type="range" min="0" max="100" value={ 100 * this.props.volume } className="slider" onChange={ this.props.onChange } />
        </div>
      );
    }
  }