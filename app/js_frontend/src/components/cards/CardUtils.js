import React from 'react'
import PropTypes from 'prop-types'
import { Grid, Divider, Typography, Box } from '@material-ui/core'

const CardHeading = ({ name }) => {
  return (
    <Grid item xs={12}>
      <Typography variant='h5' component='div'>{name}</Typography>
    </Grid >
  )
}

CardHeading.propTypes = {
  name: PropTypes.string.isRequired
}

const CardNameValuePairHeading = ({ name, on_click }) => {
  on_click = on_click === undefined ? () => { } : on_click
  return (
    <Grid item xs={3}>
      <Typography variant='body1' component='div' onClick={on_click}>
        <Box fontWeight="fontWeightBold">{name}:</Box>
      </Typography>
    </Grid>
  )
}

CardNameValuePairHeading.propTypes = {
  name: PropTypes.string.isRequired,
  on_click: PropTypes.func
}

const CardNameValuePairBrief = ({ name, value, on_click, is_vertical }) => {
  if (is_vertical) {
    return (
      <>
        <CardNameValuePairHeading name={name} on_click={on_click} />
        <Grid item xs={9}>
          {
            value.map((elem) => {
              return (<Grid item xs={12} key={elem}>{elem}</Grid>)
            })
          }
        </Grid>
      </>
    )
  }

  if (Array.isArray(value)) {
    value = '[' + value.join(', ') + ']'
  }

  if (typeof (value) === 'boolean') {
    value = value ? 'Y' : 'N'
  }

  return (
    <Grid container>
      <CardNameValuePairHeading name={name} on_click={on_click} />
      <Grid item xs={9}>
        <Typography style={{ whiteSpace: 'pre-line' }} component='div' align='justify' variant='body1'>
          {value}
        </Typography>
      </Grid>
    </Grid>
  )
}

CardNameValuePairBrief.propTypes = {
  name: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.oneOfType([PropTypes.bool, PropTypes.string, PropTypes.number])),
    PropTypes.oneOfType([PropTypes.bool, PropTypes.string, PropTypes.number])
  ]).isRequired,
  on_click: PropTypes.func,
  is_vertical: PropTypes.bool
}

const CardNameValuePairDetailed = ({ name, value, on_click, card_type, elem_props }) => {
  if (Array.isArray(value)) {
    value = `[${value.join(', ')}]`
  }

  return (
    <>
      <CardNameValuePairHeading name={name} on_click={on_click} />
      <Grid item xs={9}>
        <CardList card_type={card_type} elem_props={elem_props} />
      </Grid>
    </>
  )
}

CardNameValuePairDetailed.propTypes = {
  name: PropTypes.string.isRequired,
  value: PropTypes.arrayOf(PropTypes.oneOfType([PropTypes.string, PropTypes.number])).isRequired,
  on_click: PropTypes.func,
  card_type: PropTypes.elementType.isRequired,
  elem_props: PropTypes.PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.object),
    PropTypes.object
  ]).isRequired
}

const CardNameValuePairDynamic = ({ name, value, card_type, elem_props, is_clicked, on_click, is_vertical }) => {
  is_clicked = (is_clicked === undefined) ? () => { return false } : is_clicked
  if (is_clicked()) {
    return (
      <CardNameValuePairDetailed
        name={name} value={value} card_type={card_type} elem_props={elem_props} on_click={on_click} />
    )
  }
  return (
    <CardNameValuePairBrief
      name={name} value={value} is_vertical={is_vertical} on_click={on_click} />
  )
}

CardNameValuePairDynamic.propTypes = {
  name: PropTypes.string.isRequired,
  value: PropTypes.arrayOf(PropTypes.any).isRequired,
  card_type: PropTypes.elementType.isRequired,
  elem_props: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.object),
    PropTypes.object
  ]).isRequired,
  is_vertical: PropTypes.bool,
  is_clicked: PropTypes.func,
  on_click: PropTypes.func
}

const CardDescription = ({ desc }) => {
  return (
    <Grid item xs={12}>
      <Typography variant='body1' align='justify' component='div'>{desc}</Typography>
    </Grid>
  )
}

const CardDivider = (props) => {
  return (
    <Grid item xs={12}>
      <Divider {...props} />
    </Grid>
  )
}

CardDescription.propTypes = {
  desc: PropTypes.string.isRequired
}

const CardList = ({ card_type, elem_props }) => {
  return (
    <Grid container spacing={2}> {
      elem_props.map((elem) => {
        return (<Grid item xs={12} key={elem.name}> {card_type(elem)} </Grid>)
      })
    } </Grid>
  )
}

CardList.propTypes = {
  card_type: PropTypes.elementType.isRequired,
  elem_props: PropTypes.PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.object),
    PropTypes.object
  ]).isRequired
}

export {
  CardNameValuePairDynamic,
  CardNameValuePairDetailed,
  CardNameValuePairHeading,
  CardNameValuePairBrief,
  CardDescription,
  CardHeading,
  CardDivider,
  CardList
}
