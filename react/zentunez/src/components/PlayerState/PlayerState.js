import React, { Component } from 'react';
import { MDBContainer, MDBRow, MDBCol } from "mdbreact";


export class PlayerState extends Component {
    /**
     * This component handles the display of the album cover, along with a
     * button to update it
     */


    render(){
      var back_style = {
        backgroundImage: 'url("' + encodeURI(this.props.img_src) + '")',
      };

      return (
        <MDBContainer>
          <MDBRow><MDBCol><b>{ this.props.artist }</b></MDBCol></MDBRow>
          <MDBRow><MDBCol><b>{ this.props.album }</b></MDBCol></MDBRow>
          <MDBRow><MDBCol>{ this.props.track }</MDBCol></MDBRow>
          <MDBRow><MDBCol><b>State :</b> { this.props.state }</MDBCol></MDBRow>
          <MDBRow>
            <MDBCol><input type="range" className="custom-range"  min="0" max="100" value={ this.props.position * 100 } readOnly={ true }/></MDBCol>
          </MDBRow>
          <MDBRow>
            <MDBCol><div className="album-cover" alt="Album cover" style={ back_style } onClick={ () => window.open(this.props.img_src) }></div></MDBCol>
          </MDBRow>
        </MDBContainer>
      );
    }
  }