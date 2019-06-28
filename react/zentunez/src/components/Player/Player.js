import React, { Component } from 'react';
import { VDivider } from '../Divider/Divider.js'
import { PlayerState } from "../PlayerState/PlayerState.js"
import { VolumeSlider } from "../VolumeSlider/VolumeSlider.js"
import { TrackList } from "../TrackList/TrackList.js"
import { MDBContainer, MDBRow, MDBCol, MDBIcon } from "mdbreact";
import ReactTooltip from 'react-tooltip'

/**
 * Defines the mapping of Key values to functions
 */
class KeyMap {
  constructor() {
    this.key_map = {
      88: {"key": "x", "command": "player/play_pause"},
      90: {"key": "z", "command": "player/previous"},
      86: {"key": "v", "command": "player/stop"},
      66: {"key": "b", "command": "player/next"},
      38: {"key": "up", "command": "player/volume_up"},
      40: {"key": "down", "command": "player/volume_down"}
    }
  }

  getCommand(key_val) {
    /* Return the command given a specified key value, or *null* if
       no mapping exists.
    */
    if (key_val in this.key_map) {
      return this.key_map[key_val]["command"]
    } else {
      return null
    }
  }

  getKey(command) {
    /* Return the key to press to activate the given command. If none
       are, then return *null*.
    */
    for (var prop in this.key_map){
      if (this.key_map[prop]["command"] === command){
        return this.key_map[prop]["key"]
      }
    }
    return null
  }
}


class KeyHandler {
  /**
   * A class for handling keystrokes and sending the instructions to the
   * active media player accordingly.
   */
  constructor(player) {
    // Bind to the key event and create a list of keys to handle
    document.addEventListener("keydown", (e) => this.onKeyPress(e), false);
    this.player = player;
  }

  onKeyPress(event){
    /* Handle the keypress event. We only fire the designated action if the item
       with focus is not an input.
    */
   if (event.target.tagName !== "INPUT") {
      const key = event.keyCode;
      const km = new KeyMap()
      var command = km.getCommand(key);

      if (command != null) {
        this.player.Click(command)
      }
    }
  }

  unLoad() {
    // Remove the listening event
    document.removeEventListener("keydown", this.onKeyPress, false);
  }
}


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
                    auto_add: state.auto_add
                  };
      this.intervalID = 0;
      this.unsubscribe = props.store.subscribe(() => this.storeChanged(props.store));
    };

    storeChanged(store) {
      // React to changes in the shared stated
      var state = store.getState()
      this.setState({ api_url: state.api_url,
                      auto_add: state.auto_add });
    }

    componentDidMount() {
      // When our component loads, set the timers and start capturing keystrokes
      this.intervalID = setInterval(() => this.Click("player/state"), 1000);
      this.keyHandler = new KeyHandler(this);
    }

    componentWillUnmount() {
      // When out component unloads, destory the times and remove the keyboard hoooks
      clearInterval(this.intervalID);
      this.keyHandler.unLoad()
    }

    Click = (api_call) => {
      /* Handle the click on a Player media button */
      fetch(this.state.api_url + api_call)
        .then(res => res.json())
        .then((response) => {
            this.setState({artist: response.artist,
                          album: response.album,
                          track: response.track,
                          volume: response.volume,
                          state: response.state,
                          position: response.position,
                          img_src : this.state.api_url + "player/cover?guid=" + response.artist + response.album + response.track
                          })
        }
      )
    }

    setVolume = (vol) => {
      fetch(this.state.api_url + "player/volume_set/" + (vol.target.valueAsNumber / 100.0))
      this.Click("player/state")
    }

    renderIcon(icon, tooltip, api_call) {
      const km = new KeyMap();
      return <MDBIcon
                className="far"
                icon={ icon }
                data-tip={ tooltip + " (" + km.getKey(api_call) + ")"}
                onClick={ () => this.Click(api_call) }
              />
    }


    renderVolume() {
      return <VolumeSlider
                volume={ this.state.volume }
                onChange={ this.setVolume }
             />
    }

    renderTrackList(){
      return <TrackList
                artist={ this.state.artist }
                album={ this.state.album }
                api_url={ this.state.api_url }
                track={ this.state.track }
      />
    }

    renderState() {
      return <PlayerState
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
          <ReactTooltip />
          <MDBRow><MDBCol><b>ZenTunez Player</b></MDBCol></MDBRow>
          <MDBRow><MDBCol><VDivider /></MDBCol></MDBRow>
          <MDBRow horizontal='center'>
            <MDBCol>{this.renderIcon("fast-backward", "Previous track", "player/previous")}</MDBCol>
            <MDBCol>{this.renderIcon("stop-circle", "Stop", "player/stop")}</MDBCol>
            <MDBCol>{this.renderIcon(this.state.state === "Playing"? "pause-circle": "play-circle",
                                     "Play / Pause",
                                     "player/play_pause")}</MDBCol>
            <MDBCol>{this.renderIcon("fast-forward", "Next track", "player/next")}</MDBCol>
          </MDBRow>
          <VDivider />
          <MDBRow horizontal='center' >
            <MDBCol size="3">{this.renderIcon("volume-down", "Volume down", "player/volume_down")}</MDBCol>
            <MDBCol>{ this.renderVolume() }</MDBCol>
            <MDBCol size="3">{this.renderIcon("volume-up", "Volume up", "player/volume_up")}</MDBCol>
          </MDBRow>
          <MDBRow horizontal='center' data-tip="The currently playing track">
            { this.renderState() }
          </MDBRow>
          <MDBRow data-tip="Track listing of the current album">
            { this.renderTrackList() }
          </MDBRow>
        </MDBContainer>
      );
    }
  }
