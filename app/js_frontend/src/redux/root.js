import { combineReducers } from '@reduxjs/toolkit'

import characters_slice from 'redux/slices/characters_slice'
import effects_slice from 'redux/slices/effects_slice'
import features_slice from 'redux/slices/features_slice'
import items_slice from 'redux/slices/items_slice'
import jobs_slice from 'redux/slices/jobs_slice'
import locations_slice from 'redux/slices/locations_slice'
import npcs_slice from 'redux/slices/npcs_slice'
import options_slice from 'redux/slices/options_slice'
import spells_slice from 'redux/slices/spells_slice'

const root = combineReducers({
  characters_slice,
  effects_slice,
  features_slice,
  items_slice,
  jobs_slice,
  locations_slice,
  npcs_slice,
  options_slice,
  spells_slice
})

export default root
