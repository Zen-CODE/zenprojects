
function tunez_store(state = [], action){
  /*
  This class acts as a Redux store for the ZenTunez application settings

  In order to log state:

    for (var prop in state){
      console.log(prop + " = " + state[prop])
    }
  */

  switch (action.type) {
      case "API_URL_CHANGED":
        state["api_url"] = action.api_url;
        localStorage.setItem("api_url", action.api_url);
        return state
      case "TRACK_CHANGED":
        state["track"] = action.track;
        return state
      case "SHOW_SYS_MSG":
        var date = new Date();
        state["msg"] = action.msg;
        state["msg_type"] = action.msg_type;
        state['timestamp'] = date.toISOString();
        return state
      default:
        return state
    }
  }

  export default tunez_store