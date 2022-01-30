import { createSlice } from '@reduxjs/toolkit'

const initial_state = {
  characters: [],
  query: {}
}

const characters_slice = createSlice({
  name: 'characters_slice',
  initialState: initial_state,
  reducers: {
    set_query: (state, action) => { state.query = { ...state.query, ...action.payload } },
    set_characters: (state, action) => { state.characters = action.payload }
  }
})

export const {
  set_query,
  set_characters
} = characters_slice.actions

export default characters_slice.reducer
