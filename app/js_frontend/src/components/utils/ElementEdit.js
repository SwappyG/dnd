const handle_click = (state, state_setter, field_name, field_value) => {
  state_setter({ ...state, field_under_edit: field_name, editted_value: field_value })
}

const handle_change = (state, state_setter, change) => {
  state_setter({ ...state, ...change })
}

const on_escape_key = (state, state_setter) => {
  state_setter({
    editted_value: null,
    field_under_edit: null
  })
}

const on_enter_key = (state, state_setter) => {
  state_setter({
    editted_value: null,
    field_under_edit: null
  })
}

const on_key_down = ({ state, state_setter, event }) => {
  if (event.key === 'Escape') {
    return on_escape_key(state, state_setter)
  } else if (event.key === 'Enter') {
    return on_escape_key(state, state_setter)
  }
}

export {
  handle_click,
  handle_change,
  on_escape_key,
  on_enter_key,
  on_key_down
}
