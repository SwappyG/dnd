import React from 'react'
import PropTypes from 'prop-types'
import {
  Card,
  CardContent,
  Grid
} from '@material-ui/core'
import {
  CardDivider,
  CardHeading,
  CardNameValuePairBrief
} from 'components/cards/CardUtils'

const NPC = ({ name, gender, age, race, location, status, background, defining_moments, affiliations }) => {
  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <CardHeading name={name} />
          <CardNameValuePairBrief name='gender' value={gender} />
          <CardNameValuePairBrief name='age' value={age} />
          <CardNameValuePairBrief name='race' value={race} />
          <CardNameValuePairBrief name='location' value={location} />
          <CardNameValuePairBrief name='status' value={status} />
          <CardNameValuePairBrief name='affiliations' value={affiliations} />
          <CardDivider light />
          <CardNameValuePairBrief name='background' value={background} />
          <CardNameValuePairBrief name='defining_moments' value={defining_moments} is_vertical />
        </Grid>
      </CardContent>
    </Card >
  )
}

NPC.propTypes = {
  name: PropTypes.string.isRequired,
  gender: PropTypes.string.isRequired,
  age: PropTypes.number.isRequired,
  race: PropTypes.string.isRequired,
  location: PropTypes.string.isRequired,
  status: PropTypes.string.isRequired,
  background: PropTypes.string.isRequired,
  defining_moments: PropTypes.arrayOf(PropTypes.string).isRequired,
  affiliations: PropTypes.arrayOf(PropTypes.string).isRequired
}

export {
  NPC
}
