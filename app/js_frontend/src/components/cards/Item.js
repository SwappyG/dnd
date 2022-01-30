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

const Item = ({ name, desc }) => {
  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <CardHeading name={name} />
          <CardDivider light />
          <CardNameValuePairBrief name='desc' value={desc} />
        </Grid>
      </CardContent>
    </Card >
  )
}

Item.propTypes = {
  name: PropTypes.string.isRequired,
  desc: PropTypes.string.isRequired
}

export {
  Item
}
