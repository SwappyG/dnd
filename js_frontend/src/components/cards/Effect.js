import React from 'react'
import { createSelector } from 'reselect'
import PropTypes from 'prop-types'

import {
  Card,
  Grid,
  CardContent
} from '@material-ui/core'

import {
  CardDivider,
  CardDescription,
  CardHeading,
  CardNameValuePairBrief
} from './CardUtils'

const EffectsSelector = createSelector(
  (state, { effects, is_clicked }) => {
    if (!is_clicked) { return {} }
    return state.effects_slice.effects.filter((effect) => { return effects.includes(effect.name) })
  },
  (ii) => { return ii }
)

const Effect = ({ name, desc, effect_type, duration }) => {
  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <CardHeading name={name} />
          <CardNameValuePairBrief name='effect_type' value={effect_type} />
          <CardNameValuePairBrief name='duration' value={duration} />
          <CardDivider light />
          <CardDescription desc={desc} />
        </Grid>
      </CardContent>
    </Card>
  )
}

export const EffectProp = {
  name: PropTypes.string.isRequired,
  effect_type: PropTypes.string.isRequired,
  desc: PropTypes.string.isRequired,
  duration: PropTypes.string.isRequired
}

Effect.propTypes = EffectProp

export {
  Effect,
  EffectsSelector
}
