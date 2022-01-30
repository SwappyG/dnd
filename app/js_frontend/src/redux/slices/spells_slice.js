import { createSlice } from '@reduxjs/toolkit'

const initial_state = {
  spells: [],
  query: {}
}

const spells_slice = createSlice({
  name: 'spells_slice',
  initialState: initial_state,
  reducers: {
    set_query: (state, action) => { state.query = { ...state.query, ...action.payload } },
    set_spells: (state, action) => { state.spells = action.payload }
  }
})

export const {
  set_query,
  set_spells
} = spells_slice.actions

export default spells_slice.reducer
