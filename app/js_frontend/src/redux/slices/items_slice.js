import { createSlice } from '@reduxjs/toolkit'

const initial_state = {
  items: [],
  query: {}
}

const items_slice = createSlice({
  name: 'items_slice',
  initialState: initial_state,
  reducers: {
    set_query: (state, action) => { state.query = { ...state.query, ...action.payload } },
    set_items: (state, action) => { state.items = action.payload }
  }
})

export const {
  set_query,
  set_items
} = items_slice.actions

export default items_slice.reducer
