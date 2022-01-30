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

const Weapon = ({
  name,
  desc,
  weapon_category,
  weapon_type,
  damage_die,
  num_die,
  bonus_damage,
  damage_type,
  weapon_range,
  hit_bonus,
  weight,
  weight_category,
  two_handed,
  finesse,
  thrown,
  loading,
  ammunition
}) => {
  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <CardHeading name={name} />
          <CardNameValuePairBrief name='weapon_category' value={weapon_category} />
          <CardNameValuePairBrief name='weapon_type' value={weapon_type} />
          <CardNameValuePairBrief name='damage_die' value={damage_die} />
          <CardNameValuePairBrief name='num_die' value={num_die} />
          <CardNameValuePairBrief name='bonus_damage' value={bonus_damage} />
          <CardNameValuePairBrief name='damage_type' value={damage_type} />
          <CardNameValuePairBrief name='weapon_range' value={weapon_range} />
          <CardNameValuePairBrief name='hit_bonus' value={hit_bonus} />
          <CardNameValuePairBrief name='weight' value={weight} />
          <CardNameValuePairBrief name='weight_category' value={weight_category} />
          <CardNameValuePairBrief name='two_handed' value={two_handed} />
          <CardNameValuePairBrief name='finesse' value={finesse} />
          <CardNameValuePairBrief name='thrown' value={thrown} />
          <CardNameValuePairBrief name='loading' value={loading} />
          <CardNameValuePairBrief name='ammunition' value={ammunition} />
          <CardDivider light />
          <CardNameValuePairBrief name='desc' value={desc} />
        </Grid>
      </CardContent>
    </Card >
  )
}

Weapon.propTypes = {
  name: PropTypes.string.isRequired,
  desc: PropTypes.string.isRequired,
  weapon_category: PropTypes.string.isRequired,
  weapon_type: PropTypes.string.isRequired,
  damage_die: PropTypes.number.isRequired,
  num_die: PropTypes.number.isRequired,
  bonus_damage: PropTypes.number.isRequired,
  damage_type: PropTypes.string.isRequired,
  weapon_range: PropTypes.arrayOf(PropTypes.number).isRequired,
  hit_bonus: PropTypes.number.isRequired,
  weight: PropTypes.number.isRequired,
  weight_category: PropTypes.string.isRequired,
  two_handed: PropTypes.bool.isRequired,
  finesse: PropTypes.bool.isRequired,
  thrown: PropTypes.bool.isRequired,
  loading: PropTypes.bool.isRequired,
  ammunition: PropTypes.bool.isRequired
}

export {
  Weapon
}
