import { createSlice } from '@reduxjs/toolkit'

const initial_state = {
  options: [],
  query: {}
}

const options_slice = createSlice({
  name: 'options_slice',
  initialState: initial_state,
  reducers: {
    set_query: (state, action) => { state.query = { ...state.query, ...action.payload } },
    set_options: (state, action) => { state.options = action.payload }
  }
})

export const {
  set_query,
  set_options
} = options_slice.actions

export default options_slice.reducer
