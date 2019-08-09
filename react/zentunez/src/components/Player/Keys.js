/**
 * Defines the mapping of Key values to functions
 */
export class KeyMap {
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


  export class KeyHandler {
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
       if (!(event.shiftKey || event.ctrlKey || event.altKey)) {
          const key = event.keyCode;
          const km = new KeyMap()
          var command = km.getCommand(key);

          if (command != null) {
            this.player.send_system_command(command, key);
          }
       }
      }
    }

    unLoad() {
      // Remove the listening event
      document.removeEventListener("keydown", this.onKeyPress, false);
    }
  }
