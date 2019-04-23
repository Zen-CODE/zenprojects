import React, { Component } from 'react';
import {Divider} from "../Divider/Divider.js"


export class PlayerImage extends Component {
    /**
     * This component handles the display of the album cover, along with a
     * button to update it
     */
    constructor(props) {
      super(props);
      this.state = {img_src: "", };
    };
  
    onClick(){
      /** 
       * Fetch the album cover and
      */
      const url = "http://127.0.0.1:5000/tunez/api/v1.0/"
      this.setState({img_src: url + "player/cover"});
    }
  
    render(){
      return (
        <div>
          <div>
            <button onClick={ () => this.onClick() }>Fetch Image</button>
          </div>
          <Divider />
          <div>
            <img alt="Album cover" src={this.state.img_src}></img>
          </div>
        </div>
      );
    }
  }