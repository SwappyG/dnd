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

const SkillProficiencies = ({
  athletics,
  acrobatics,
  animal_handling,
  arcana,
  deception,
  history,
  insight,
  intimidation,
  investigation,
  medicine,
  nature,
  perception,
  performance,
  persuasion,
  religion,
  sleight_of_hand,
  stealth,
  survival
}) => {
  return (
    <Card>
      <CardContent>
        <Grid container>
          <CardNameValuePairBrief name='athletics' value={athletics} />
          <CardNameValuePairBrief name='acrobatics' value={acrobatics} />
          <CardNameValuePairBrief name='animal_handling' value={animal_handling} />
          <CardNameValuePairBrief name='arcana' value={arcana} />
          <CardNameValuePairBrief name='deception' value={deception} />
          <CardNameValuePairBrief name='history' value={history} />
          <CardNameValuePairBrief name='insight' value={insight} />
          <CardNameValuePairBrief name='intimidation' value={intimidation} />
          <CardNameValuePairBrief name='investigation' value={investigation} />
          <CardNameValuePairBrief name='medicine' value={medicine} />
          <CardNameValuePairBrief name='nature' value={nature} />
          <CardNameValuePairBrief name='perception' value={perception} />
          <CardNameValuePairBrief name='performance' value={performance} />
          <CardNameValuePairBrief name='persuasion' value={persuasion} />
          <CardNameValuePairBrief name='religion' value={religion} />
          <CardNameValuePairBrief name='sleight_of_hand' value={sleight_of_hand} />
          <CardNameValuePairBrief name='stealth' value={stealth} />
          <CardNameValuePairBrief name='survival' value={survival} />
        </Grid>
      </CardContent>
    </Card >
  )
}

SkillProficiencies.propTypes = {
  athletics: PropTypes.number.isRequired,
  acrobatics: PropTypes.number.isRequired,
  animal_handling: PropTypes.number.isRequired,
  arcana: PropTypes.number.isRequired,
  deception: PropTypes.number.isRequired,
  history: PropTypes.number.isRequired,
  insight: PropTypes.number.isRequired,
  intimidation: PropTypes.number.isRequired,
  investigation: PropTypes.number.isRequired,
  medicine: PropTypes.number.isRequired,
  nature: PropTypes.number.isRequired,
  perception: PropTypes.number.isRequired,
  performance: PropTypes.number.isRequired,
  persuasion: PropTypes.number.isRequired,
  religion: PropTypes.number.isRequired,
  sleight_of_hand: PropTypes.number.isRequired,
  stealth: PropTypes.number.isRequired,
  survival: PropTypes.number.isRequired
}

export {
  SkillProficiencies
}
