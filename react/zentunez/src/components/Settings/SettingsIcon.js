import React, { Component } from 'react';
import { MDBContainer, MDBRow, MDBCol, MDBIcon } from "mdbreact";

export class SettingsIcon extends Component {
    /**
     * This component displays the settings icon
     */    
    constructor(props) {
        super(props);
        this.state = {music_folder: "~/Music",
                      username: props.username}
      };

    onClick()  {
        /* Respond to the clicking of the settings icon */
        console.log("Settings click")
    }


    render(){        
      return <div className="settings-icon">
          <MDBContainer>
            <MDBRow>
              <MDBCol>
                <MDBIcon 
                  className="far"
                  icon="cogs"
                  onClick={ () => this.onClick() }
                  />
                </MDBCol>
                <MDBCol>
                  <p>{ this.state.username }</p>
                </MDBCol>
              </MDBRow>
            </MDBContainer>
          </div>
    }
  }