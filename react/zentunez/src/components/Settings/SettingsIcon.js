import React, { Component } from 'react';
import { MDBIcon } from "mdbreact";


export class SettingsIcon extends Component {
    /**
     * This component displays the settings icon
     */    
    constructor(props) {
        super(props);
        this.state = {music_folder: "~/Music"}
      };

    onClick()  {
        /* Respond to the clicking of the settings icon */
        console.log("Settings click")
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