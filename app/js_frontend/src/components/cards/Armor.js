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

const Armor = ({ name, desc, armor_type, ac, minimum_strength, has_stealth_disadvantage }) => {
  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <CardHeading name={name} />
          <CardNameValuePairBrief name='armor_type' value={armor_type} />
          <CardNameValuePairBrief name='ac' value={ac} />
          <CardNameValuePairBrief name='min_str' value={minimum_strength} />
          <CardNameValuePairBrief name='stealth_disadv' value={has_stealth_disadvantage} />
          <CardDivider light />
          <CardNameValuePairBrief name='desc' value={desc} />
        </Grid>
      </CardContent>
    </Card >
  )
}

Armor.propTypes = {
  name: PropTypes.string.isRequired,
  desc: PropTypes.string.isRequired,
  armor_type: PropTypes.string.isRequired,
  ac: PropTypes.number.isRequired,
  minimum_strength: PropTypes.number.isRequired,
  has_stealth_disadvantage: PropTypes.bool.isRequired
}

export {
  Armor
}
