import React, { useState } from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import {
  Card,
  CardContent,
  Grid
} from '@material-ui/core'
import { FeatureStatic } from 'components/cards/Feature'
import {
  CardDivider,
  CardHeading,
  CardDescription,
  CardNameValuePairBrief,
  CardNameValuePairDynamic
} from 'components/cards/CardUtils'

const OptionStatic = ({ name, desc, features, prereq_features, unlock_levels }) => {
  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <CardHeading name={name} />
          <CardNameValuePairBrief name='unlock_levels' value={unlock_levels} />
          <CardNameValuePairBrief name='features' value={features} is_vertical={true} />
          <CardNameValuePairBrief name='prereq_features' value={prereq_features} is_vertical={true} />
          <CardDivider light />
          <CardDescription desc={desc} />
        </Grid>
      </CardContent>
    </Card>
  )
}

OptionStatic.propTypes = {
  name: PropTypes.string.isRequired,
  desc: PropTypes.string.isRequired,
  features: PropTypes.arrayOf(PropTypes.string).isRequired,
  prereq_features: PropTypes.arrayOf(PropTypes.string).isRequired,
  unlock_levels: PropTypes.arrayOf(PropTypes.number).isRequired
}

const Option = ({ name, desc, features, prereq_features, unlock_levels }) => {
  const [state, setState] = useState({
    is_features_clicked: false,
    is_prereq_features_clicked: false
  })

  const features_props = useSelector((state) => {
    return state.features_slice.features.filter(
      (feature) => { return features.includes(feature.name) }
    )
  })

  const prereq_features_props = useSelector((state) => {
    return state.features_slice.features.filter(
      (feature) => { return prereq_features.includes(feature.name) }
    )
  })

  return (
    <div>
      <Card>
        <CardContent>
          <Grid container spacing={1}>
            <CardHeading name={name} />
            <CardNameValuePairBrief name='unlock_levels' value={unlock_levels} is_vertical={false} />
            <CardNameValuePairDynamic
              name='features' value={features} card_type={FeatureStatic} elem_props={features_props} is_vertical
              is_clicked={() => { return state.is_features_clicked }}
              on_click={() => { setState({ ...state, is_features_clicked: !state.is_features_clicked }) }} />
            <CardNameValuePairDynamic
              name='prereq_features' value={prereq_features} card_type={FeatureStatic} elem_props={prereq_features_props} is_vertical
              is_clicked={() => { return state.is_prereq_features_clicked }}
              on_click={() => { setState({ ...state, is_prereq_features_clicked: !state.is_prereq_features_clicked }) }} />
            <CardDivider light />
            <CardDescription desc={desc} />
          </Grid>
        </CardContent>
      </Card>
    </div>
  )
}

Option.propTypes = {
  name: PropTypes.string.isRequired,
  desc: PropTypes.string.isRequired,
  features: PropTypes.arrayOf(PropTypes.string).isRequired,
  prereq_features: PropTypes.arrayOf(PropTypes.string).isRequired,
  unlock_levels: PropTypes.arrayOf(PropTypes.number).isRequired
}

export {
  Option,
  OptionStatic
}
