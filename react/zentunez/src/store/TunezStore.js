
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
      case "SHOW_SYS_INFO_CHANGED":
        console.log("Store: Changing show_sys_info to " + action.show_sys_info);
        state["show_sys_info"] = action.show_sys_info;
        localStorage.setItem("show_sys_info", action.show_sys_info);
        return state
      default:
        return state
    }
  }

  export default tunez_store