import React from 'react'
import PropTypes from 'prop-types'
import { Grid, Divider, Typography, Box } from '@material-ui/core'

const CardHeading = ({ name }) => {
  return (
    <Grid xs={12}>
      <Typography variant='h5' component='div'>{name}</Typography>
    </Grid >
  )
}

CardHeading.propTypes = {
  name: PropTypes.string.isRequired
}

const CardNameValuePairHeading = ({ name, value, on_click }) => {
  on_click = on_click === undefined ? (name, value) => { } : on_click
  return (
    <Grid item xs={2}>
      <Typography variant='body1' component='div' onClick={() => on_click(name, value)}>
        <Box fontWeight="fontWeightBold">{name}:</Box>
      </Typography>
    </Grid>
  )
}

CardNameValuePairHeading.propTypes = {
  name: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  on_click: PropTypes.func
}

const CardNameValuePairBrief = ({ name, value, on_click, is_vertical }) => {
  if (is_vertical) {
    return (
      <Grid item xs={12}>
        <Grid container>
          <CardNameValuePairHeading name={name} value={value} on_click={on_click} />
          <Grid item xs={10}> {value.map((elem) => {
            return (<Grid xs={12} key={elem}>- {elem}</Grid>)
          })}</Grid>
        </Grid>
      </Grid>
    )
  }

  if (Array.isArray(value)) {
    value = '[' + value.join(', ') + ']'
  }

  return (
    <Grid item xs={12} >
      <Grid container>
        <CardNameValuePairHeading name={name} value={value} on_click={on_click} />
        <Grid item xs={10}>{value}</Grid>
      </Grid>
    </Grid>
  )
}

CardNameValuePairBrief.propTypes = {
  name: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  on_click: PropTypes.func,
  is_vertical: PropTypes.bool.isRequired
}

const CardNameValuePairDetailed = ({ name, value, on_click, card_type, elem_props }) => {
  if (Array.isArray(value)) {
    value = `[${value.join(', ')}]`
  }

  return (
    <Grid container spacing={1}>
      <CardNameValuePairHeading name={name} value={value} on_click={() => { on_click(name, value) }} />
      <Grid item xs={10}>
        <CardList card_type={card_type} elem_props={elem_props} />
      </Grid>
    </Grid>
  )
}

CardNameValuePairDetailed.propTypes = {
  name: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  on_click: PropTypes.func,
  card_type: PropTypes.elementType.isRequired,
  elem_props: PropTypes.object.isRequired
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
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  card_type: PropTypes.elementType.isRequired,
  elem_props: PropTypes.object.isRequired,
  is_vertical: PropTypes.bool.isRequired,
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
        return (
          <Grid item xs={12} key={elem.name}>
            {card_type(elem)}
          </Grid>
        )
      })
    } </Grid>
  )
}

CardList.propTypes = {
  card_type: PropTypes.elementType.isRequired,
  elem_props: PropTypes.object.isRequired
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
