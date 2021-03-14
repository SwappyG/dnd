import React, { useState } from 'react'
import { useSelector } from 'react-redux'
import { createSelector } from 'reselect'
import PropTypes from 'prop-types'
import { Card, Grid, CardContent } from '@material-ui/core'
import { Effect, EffectsSelector } from 'components/cards/Effect'
import {
  CardDivider,
  CardHeading,
  CardDescription,
  CardNameValuePairBrief,
  CardNameValuePairDynamic
} from 'components/cards/CardUtils'

const FeaturesSelector = createSelector(
  (state, { features, is_clicked }) => {
    if (!is_clicked) { return {} }
    return state.features_slice.features.filter((feature) => { return features.includes(feature.name) })
  },
  (ii) => { return ii }
)

const FeatureStatic = ({ name, unlock_level, effects, prereq_features, desc }) => {
  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <CardHeading name={name} />
          <CardNameValuePairBrief name='unlock_level' value={unlock_level} />
          <CardNameValuePairBrief name='effects' value={effects} is_vertical={true} />
          <CardNameValuePairBrief name='prereq_features' value={prereq_features} is_vertical={true} />
          <CardDivider light />
          <CardDescription desc={desc} />
        </Grid>
      </CardContent>
    </Card>
  )
}

const feature_prop_types = {
  name: PropTypes.string.isRequired,
  desc: PropTypes.string.isRequired,
  effects: PropTypes.arrayOf(PropTypes.string).isRequired,
  prereq_features: PropTypes.arrayOf(PropTypes.string).isRequired,
  unlock_level: PropTypes.number
}

FeatureStatic.propTypes = feature_prop_types

const Feature = ({ name, effects, prereq_features, unlock_level, desc }) => {
  const [state, setState] = useState({
    is_effects_clicked: false,
    is_prereq_features_clicked: false
  })

  const effects_props = useSelector((store_state) => {
    return EffectsSelector(store_state, {
      is_clicked: state.is_effects_clicked,
      effects: effects
    })
  })

  const prereq_features_props = useSelector((store_state) => {
    return FeaturesSelector(store_state, {
      is_clicked: state.is_prereq_features_clicked,
      features: prereq_features
    })
  })

  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <CardHeading name={name} />
          <CardNameValuePairBrief name='unlock_level' value={unlock_level} is_vertical={false} />
          <CardNameValuePairDynamic
            name='effects' value={effects} card_type={Effect} elem_props={effects_props}
            is_vertical={true}
            is_clicked={() => { return state.is_effects_clicked }}
            on_click={() => { setState({ ...state, is_effects_clicked: !state.is_effects_clicked }) }} />
          <CardNameValuePairDynamic
            name='prereq_features' value={prereq_features} card_type={FeatureStatic} elem_props={prereq_features_props}
            is_vertical={true}
            is_clicked={() => { return state.is_prereq_features_clicked }}
            on_click={() => { setState({ ...state, is_prereq_features_clicked: !state.is_prereq_features_clicked }) }} />
          <CardDivider light />
          <CardDescription desc={desc} />
        </Grid>
      </CardContent>
    </Card>
  )
}

Feature.propTypes = feature_prop_types

export {
  Feature,
  FeatureStatic,
  FeaturesSelector
}
