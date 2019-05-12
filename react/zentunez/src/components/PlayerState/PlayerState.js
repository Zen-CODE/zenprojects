import React, { Component } from 'react';
import { MDBContainer, MDBRow, MDBCol } from "mdbreact";


export class PlayerState extends Component {
    /**
     * This component handles the display of the album cover, along with a
     * button to update it
     */    


    render(){
      return (
        <MDBContainer>
          <MDBRow><MDBCol><b>Track: </b> { this.props.track }</MDBCol></MDBRow>
          <MDBRow><MDBCol><b>State :</b> { this.props.state }</MDBCol></MDBRow>
          <MDBRow>
            <MDBCol><input type="range" className="custom-range"  min="0" max="100" value={ this.props.position * 100 } readOnly={ true }/></MDBCol>
          </MDBRow>
          <MDBRow>
            <MDBCol><img className="album-cover" alt="Album cover" src={ this.props.img_src } onClick={ () => window.open(this.props.img_src) }></img></MDBCol>
          </MDBRow>
        </MDBContainer>
      );
    }
  }