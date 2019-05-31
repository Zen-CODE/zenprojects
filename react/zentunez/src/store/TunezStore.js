
function tunez_store(state = [], action){
  /*
  This class acts as a Redux store for the ZenTunez application settings
  */
  console.log("tunez_store: action = " + action.type);
  switch (action.type) {
      case 'ADD_TODO':
        return [
          ...state,
          {
            id: action.id,
            text: action.text,
            completed: false
          }
        ]
      case 'TOGGLE_TODO':
        return state.map(todo =>
          todo.id === action.id ? { ...todo, completed: !todo.completed } : todo
        )
      default:
        return state
    }
  }

  export default tunez_store