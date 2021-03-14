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

const Location = ({ name, loc_type, country, population, climate, status, leader, races, desc }) => {
  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <CardHeading name={name} />
          <CardNameValuePairBrief name='country' value={country} />
          <CardNameValuePairBrief name='population' value={population} />
          <CardNameValuePairBrief name='loc_type' value={loc_type} />
          <CardNameValuePairBrief name='climate' value={climate} />
          <CardNameValuePairBrief name='status' value={status} />
          <CardNameValuePairBrief name='leader' value={leader} />
          <CardNameValuePairBrief name='races' value={races} is_vertical />
          <CardDivider light />
          <CardNameValuePairBrief name='desc' value={desc} />
        </Grid>
      </CardContent>
    </Card >
  )
}

Location.propTypes = {
  name: PropTypes.string.isRequired,
  desc: PropTypes.string.isRequired,
  loc_type: PropTypes.string.isRequired,
  races: PropTypes.arrayOf(PropTypes.string).isRequired,
  climate: PropTypes.number.isRequired,
  population: PropTypes.number.isRequired,
  status: PropTypes.string.isRequired,
  country: PropTypes.string.isRequired,
  leader: PropTypes.string
}

export {
  Location
}
