import React, { useState } from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import {
  Card,
  CardContent,
  Grid
} from '@material-ui/core'
import { FeatureStatic } from 'components/cards/Feature'
import { OptionStatic } from 'components/cards/Option'
import {
  CardDivider,
  CardHeading,
  CardDescription,
  CardNameValuePairDynamic
} from 'components/cards/CardUtils'

const Job = ({ name, features, options, desc }) => {
  const [state, setState] = useState({
    is_features_selected: false,
    is_options_selected: false
  })

  const features_props = useSelector((state) => {
    return state.features_slice.features.filter(
      (feature) => { return features.includes(feature.name) }
    )
  })

  const options_props = useSelector((state) => {
    return state.options_slice.options.filter(
      (option) => { return options.includes(option.name) }
    )
  })

  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <CardHeading name={name} />
          <CardNameValuePairDynamic name='features' value={features} card_type={FeatureStatic}
            elem_props={features_props} is_vertical={true}
            is_clicked={() => { return state.is_features_clicked }}
            on_click={() => { setState({ ...state, is_features_clicked: !state.is_features_clicked }) }} />

          <CardNameValuePairDynamic name='options' value={options} card_type={OptionStatic}
            elem_props={options_props} is_vertical={true}
            is_clicked={() => { return state.is_options_selected }}
            on_click={() => { setState({ ...state, is_options_selected: !state.is_options_selected }) }} />

          <CardDivider light />

          <CardDescription desc={desc} />
        </Grid>
      </CardContent>
    </Card>
  )
}

export const JobProp = {
  name: PropTypes.string.isRequired,
  desc: PropTypes.string.isRequired,
  features: PropTypes.arrayOf(PropTypes.string).isRequired,
  options: PropTypes.arrayOf(PropTypes.string).isRequired
}

Job.propTypes = JobProp

export {
  Job
}
