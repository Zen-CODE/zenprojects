import React, { Component } from 'react';
import { MDBContainer, MDBRow, MDBCol } from "mdbreact";


export class PlayerState extends Component {
    /**
     * This component handles the display of the album cover, along with a
     * button to update it
     */


    render(){
      //var img = ""; // "http://127.0.0.1:8000/library/cover/Professor%20Trance%20And%20The%20Energisers/Shaman'S%20Breath";
      // var img = "http://127.0.0.1:8000/library/cover/Affiance/Blackout";
      var img = encodeURI(this.props.img_src);
      console.log("Player State: image=" + this.props.img_src);

      var back_style = {
        // backgroundImage: "url(http://127.0.0.1:8000/library/cover/Professor%20Trance%20And%20The%20Energisers/Shaman'S%20Breath)"
        // backgroundImage: "url(" + this.props.img_src + ")"
        backgroundImage: "url(" + img + ")",
        height: '400px',
        backgroundSize: 'contain',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center'
      };

      // <MDBCol><div alt="Album cover" style={ back_style } onClick={ () => window.open(this.props.img_src) }></div></MDBCol>
      return (
        <MDBContainer>
          <MDBRow><MDBCol><b>Track: </b> { this.props.track }</MDBCol></MDBRow>
          <MDBRow><MDBCol><b>State :</b> { this.props.state }</MDBCol></MDBRow>
          <MDBRow>
            <MDBCol><input type="range" className="custom-range"  min="0" max="100" value={ this.props.position * 100 } readOnly={ true }/></MDBCol>
          </MDBRow>
          <MDBRow>
            <MDBCol><div alt="Album cover" style={{ backgroundImage: "url(" + `${img}` + ")", height: "400px" }} onClick={ () => window.open(this.props.img_src) }></div></MDBCol>
          </MDBRow>
        </MDBContainer>
      );
    }
  }