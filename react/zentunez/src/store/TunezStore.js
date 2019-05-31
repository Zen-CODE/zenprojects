
function tunez_store(state = [], action){
  /*
  This class acts as a Redux store for the ZenTunez application settings
  */
  console.log("tunez_store: action = " + action.type);
  for (var prop in state){
    console.log(prop + " = " + state[prop])
  }

  switch (action.type) {
      case "API_URL_CHANGED":
        console.log("API_URL_CHANGED. state = " + state)
        state["api_url"] = action.api_url;
        return state
        // return [
        //   ...state,
        //   { api_url: action.api_url }
        // ]
      case 'TOGGLE_TODO':
        return state.map(todo =>
          todo.id === action.id ? { ...todo, completed: !todo.completed } : todo
        )
      default:
        return state
    }
  }

  export default tunez_store