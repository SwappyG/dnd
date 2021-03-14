import { createSlice } from '@reduxjs/toolkit'

const initial_state = {
  features: [],
  query: {}
}

const features_slice = createSlice({
  name: 'features_slice',
  initialState: initial_state,
  reducers: {
    set_query: (state, action) => { state.query = { ...state.query, ...action.payload } },
    set_features: (state, action) => { state.features = action.payload }
  }
})

export const {
  set_query,
  set_features
} = features_slice.actions

export default features_slice.reducer
