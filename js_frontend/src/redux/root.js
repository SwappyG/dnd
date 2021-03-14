import { combineReducers } from '@reduxjs/toolkit'

import effects_slice from 'redux/slices/effects_slice'
import features_slice from 'redux/slices/features_slice'
import jobs_slice from 'redux/slices/jobs_slice'
import npcs_slice from 'redux/slices/npcs_slice'
import locations_slice from 'redux/slices/locations_slice'
import spells_slice from 'redux/slices/spells_slice'
import options_slice from 'redux/slices/options_slice'

const root = combineReducers({
  effects_slice,
  features_slice,
  jobs_slice,
  npcs_slice,
  locations_slice,
  spells_slice,
  options_slice
})

export default root
