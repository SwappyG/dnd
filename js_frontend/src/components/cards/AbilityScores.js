import React from 'react'
import PropTypes from 'prop-types'
import {
  Card,
  CardContent,
  Grid
} from '@material-ui/core'
import {
  CardNameValuePairBrief
} from 'components/cards/CardUtils'

const AbilityScore = ({ STR, DEX, CON, INT, WIS, CHA }) => {
  return (
    <Card>
      <CardContent>
        <Grid container>
          <CardNameValuePairBrief name='STR' value={STR} />
          <CardNameValuePairBrief name='DEX' value={DEX} />
          <CardNameValuePairBrief name='CON' value={CON} />
          <CardNameValuePairBrief name='INT' value={INT} />
          <CardNameValuePairBrief name='WIS' value={WIS} />
          <CardNameValuePairBrief name='CHA' value={CHA} />
        </Grid>
      </CardContent>
    </Card >
  )
}

AbilityScore.propTypes = {
  STR: PropTypes.string.isRequired,
  DEX: PropTypes.string.isRequired,
  CON: PropTypes.string.isRequired,
  INT: PropTypes.string.isRequired,
  WIS: PropTypes.string.isRequired,
  CHA: PropTypes.string.isRequired
}

export {
  AbilityScore
}
