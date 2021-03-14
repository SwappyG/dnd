import { createSlice } from '@reduxjs/toolkit'

const initial_state = {
  locations: [],
  query: {}
}

const locations_slice = createSlice({
  name: 'locations_slice',
  initialState: initial_state,
  reducers: {
    set_query: (state, action) => { state.query = { ...state.query, ...action.payload } },
    set_locations: (state, action) => { state.locations = action.payload }
  }
})

export const {
  set_query,
  set_locations
} = locations_slice.actions

export default locations_slice.reducer
