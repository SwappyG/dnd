import { createSlice } from '@reduxjs/toolkit'

const initial_state = {
  jobs: [],
  query: {}
}

const jobs_slice = createSlice({
  name: 'jobs_slice',
  initialState: initial_state,
  reducers: {
    set_query: (state, action) => { state.query = { ...state.query, ...action.payload } },
    set_jobs: (state, action) => { state.jobs = action.payload }
  }
})

export const {
  set_query,
  set_jobs
} = jobs_slice.actions

export default jobs_slice.reducer
