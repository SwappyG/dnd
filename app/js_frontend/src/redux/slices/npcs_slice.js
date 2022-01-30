import { createSlice } from '@reduxjs/toolkit'

const initial_state = {
  npcs: [],
  query: {}
}

const npcs_slice = createSlice({
  name: 'npcs_slice',
  initialState: initial_state,
  reducers: {
    set_query: (state, action) => { state.query = { ...state.query, ...action.payload } },
    set_npcs: (state, action) => { state.npcs = action.payload }
  }
})

export const {
  set_query,
  set_npcs
} = npcs_slice.actions

export default npcs_slice.reducer
