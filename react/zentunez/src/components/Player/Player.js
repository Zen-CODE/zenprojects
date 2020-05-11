import React, { Component } from 'react';
import { VDivider } from '../Divider/Divider.js'
import { PlayerState } from "../PlayerState/PlayerState.js"
import { VolumeSlider } from "../VolumeSlider/VolumeSlider.js"
import { TrackMeta } from "../TrackMeta/TrackMeta.js"
import { MDBContainer, MDBRow, MDBCol, MDBIcon } from "mdbreact";
import { send_message } from "../SysMsg/SysMsg.js"
import { queued_fetch } from "../../functions/network.js"
import { KeyMap,  KeyHandler } from "./Keys.js"


export class Player extends Component {
    /*
    This class houses functionality to control the currently playting MPRIS2
    audio player and retreive state information from it.
    */
   constructor(props) {
      super(props);
      var state = props.store.getState();
      this.state = {artist: "-",
                    album: "-",
                    track: "-",
                    volume: 0,
                    state: "-",
                    position: 0,
                    img_src: "",
                    api_url: state.api_url,
                    store: props.store

                  };
      this.intervalID = 0;
      this.unsubscribe = props.store.subscribe(() => this.storeChanged(props.store));
    };

    send_system_command(command, msg) {
        // Send the *command* message to the plater and then display the *msg*
        this.Click(command, true);
        send_message(this.state.store, msg, "command")
    }

    storeChanged(store) {
      // React to changes in the shared stated
      var state = store.getState()
      this.setState({ api_url: state.api_url });
    }

    componentDidMount() {
      // When our component loads, set the timers and start capturing keystrokes
      this.intervalID = setInterval(() => this.Click("zenplayer/get_state"), 1000);
      this.keyHandler = new KeyHandler(this);
    }

    componentWillUnmount() {
      // When out component unloads, destory the times and remove the keyboard hoooks
      clearInterval(this.intervalID);
      this.keyHandler.unLoad()
      this.unsubscribe()
    }

    /**
     * Handle the click on a Player media button. This access a *api_call*
     * papameter which defines the action to be taken.
     *
     * @param {string} api_call - The path of the endpoint to call with arguments
     */
    Click = (api_call, force=false) => {
      // First we define a callback function to acceptg the JSON response
      const update_state = (response) => {
        if (this.state.track !== response.track){
          this.state.store.dispatch({ type: "TRACK_CHANGED",
                                      track: response.track })
        };
        this.setState({artist: response.artist,
                      album: response.album,
                      track: response.track,
                      volume: response.volume,
                      state: response.state,
                      position: response.position,
                      img_src : this.state.api_url + `zenplayer/get_track_cover?cover=${encodeURIComponent(response.cover)}`
                      })
        if ("message" in response) {
          send_message(this.state.store, response.message.text, "event");
        };
      }

      // Then we queue the request and supply the callback
      queued_fetch(this.state.api_url + api_call);
      queued_fetch(this.state.api_url + "zenplayer/get_state", update_state, force);
    }

    setVolume = (vol) => {
      queued_fetch(this.state.api_url + "zenplayer/volume_set?volume=" + (vol.target.valueAsNumber / 100.0),
                  null,
                  true);
      this.send_system_command("player/state", "Changing volume...");
    }

    renderIcon(icon, tooltip, api_call) {
      const km = new KeyMap();
      return <MDBIcon
                className="far"
                icon={ icon }
                data-tip={ tooltip + " (" + km.getKey(api_call) + ")"}
                onClick={ () => this.send_system_command(api_call, tooltip) }
              />
    }


    renderVolume() {
      return <VolumeSlider
                volume={ this.state.volume }
                onChange={ this.setVolume }
             />
    }

    renderTrackMeta(){
      return <TrackMeta
                artist={ this.state.artist }
                album={ this.state.album }
                api_url={ this.state.api_url }
                track={ this.state.track }
      />
    }

    renderState() {
      return <PlayerState
        artist={ this.state.artist }
        album={ this.state.album }
        track={ this.state.track }
        position={ this.state.position }
        state={ this.state.state }
        img_src={ this.state.img_src }
      />
    }

    render() {
      /**
       * The main application objects are build and returned here.
      */
      return (
        <MDBContainer>
          <MDBRow><MDBCol><b>ZenTunez Player</b></MDBCol></MDBRow>
          <MDBRow><MDBCol><VDivider /></MDBCol></MDBRow>
          <MDBRow horizontal='center'>
            <MDBCol>{this.renderIcon("fast-backward", "Previous track", "zenplayer/play_previous")}</MDBCol>
            <MDBCol>{this.renderIcon("stop-circle", "Stop", "zenplayer/stop")}</MDBCol>
            <MDBCol>{this.renderIcon(this.state.state === "Playing"? "pause-circle": "play-circle",
                                     "Play / Pause",
                                     "zenplayer/play_pause")}</MDBCol>
            <MDBCol>{this.renderIcon("fast-forward", "Next track", "zenplayer/play_next")}</MDBCol>
          </MDBRow>
          <VDivider />
          <MDBRow horizontal='center' >
            <MDBCol size="3">{this.renderIcon("volume-down", "Volume down", "zenplayer/volume_down")}</MDBCol>
            <MDBCol>{ this.renderVolume() }</MDBCol>
            <MDBCol size="3">{this.renderIcon("volume-up", "Volume up", "zenplayer/volume_up")}</MDBCol>
          </MDBRow>
          <MDBRow horizontal='center' data-tip="The currently playing track">
            { this.renderState() }
          </MDBRow>
          <MDBRow data-tip="Track listing of the current album">
            { this.renderTrackMeta() }
          </MDBRow>
        </MDBContainer>
      );
    }
  }
