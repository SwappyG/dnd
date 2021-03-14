import { createSlice } from '@reduxjs/toolkit'

const initial_state = {
  effects: [],
  query: {}
}

const effect_slice = createSlice({
  name: 'effect_slice',
  initialState: initial_state,
  reducers: {
    set_query: (state, action) => { state.query = { ...state.query, ...action.payload } },
    set_effects: (state, action) => { state.effects = action.payload }
  }
})

export const {
  set_query,
  set_effects
} = effect_slice.actions

export default effect_slice.reducer
