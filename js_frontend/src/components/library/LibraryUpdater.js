import React, { useEffect } from 'react'
import PropTypes from 'prop-types'
import { Grid } from '@material-ui/core'
import { useDispatch, useSelector } from 'react-redux'

import { set_characters } from 'redux/slices/characters_slice'
import { set_effects } from 'redux/slices/effects_slice'
import { set_features } from 'redux/slices/features_slice'
import { set_items } from 'redux/slices/items_slice'
import { set_jobs } from 'redux/slices/jobs_slice'
import { set_locations } from 'redux/slices/locations_slice'
import { set_npcs } from 'redux/slices/npcs_slice'
import { set_options } from 'redux/slices/options_slice'
// import { set_spells } from 'redux/slices/spells_slice'

const fetch_json = (address, port, lib_name, data_setter, dispatcher) => {
  return fetch(`http://${address}:${port}/library/${lib_name}`).then((res) => {
    res.json().then((data) => {
      dispatcher(data_setter(data.data))
    }).catch(e => {
      console.error(e)
    })
  }).catch(e => {
    console.error(e)
  })
}

const UpdaterImpl = ({ address, port, library_name, state_field, setter }) => {
  const dispatcher = useDispatch()
  const { query } = useSelector((state) => state[state_field])
  useEffect(() => { fetch_json(address, port, library_name, setter, dispatcher) }, [query])
  return (
    <Grid item xs={12} />
  )
}

const LibraryUpdater = (props) => {
  UpdaterImpl({ ...props, library_name: 'characters', state_field: 'characters_slice', setter: set_characters })
  UpdaterImpl({ ...props, library_name: 'effects', state_field: 'effects_slice', setter: set_effects })
  UpdaterImpl({ ...props, library_name: 'features', state_field: 'features_slice', setter: set_features })
  UpdaterImpl({ ...props, library_name: 'items', state_field: 'items_slice', setter: set_items })
  UpdaterImpl({ ...props, library_name: 'jobs', state_field: 'jobs_slice', setter: set_jobs })
  UpdaterImpl({ ...props, library_name: 'locations', state_field: 'locations_slice', setter: set_locations })
  UpdaterImpl({ ...props, library_name: 'npcs', state_field: 'npcs_slice', setter: set_npcs })
  UpdaterImpl({ ...props, library_name: 'options', state_field: 'options_slice', setter: set_options })
  return (
    <Grid item xs={12} />
  )
}

UpdaterImpl.propTypes = {
  address: PropTypes.string.isRequired,
  port: PropTypes.string.isRequired,
  library_name: PropTypes.string.isRequired,
  state_field: PropTypes.string.isRequired,
  setter: PropTypes.object.isRequired
}

LibraryUpdater.propTypes = {
  address: PropTypes.string.isRequired,
  port: PropTypes.number.isRequired
}

export {
  LibraryUpdater
}
