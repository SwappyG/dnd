import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'
import {
  Card,
  CardContent,
  Grid
} from '@material-ui/core'

import {
  CardDivider,
  CardHeading,
  CardNameValuePairBrief,
  CardNameValuePairDynamic
} from 'components/cards/CardUtils'

import { FeatureStatic, FeaturesSelector } from 'components/cards/Feature'
import { AbilityScore } from 'components/cards/AbilityScores'
import { SkillProficiencies } from 'components/cards/SkillProficiencies'

const Character = ({
  name,
  job,
  age,
  gender,
  alignment,
  level,
  sub_level,
  bio,
  ability_score,
  skills,
  max_hp,
  hit_die,
  learned_features,
  learned_spells,
  spell_slots
}) => {
  const [state, setState] = useState({
    is_learned_features_clicked: false,
    is_learned_spells_clicked: false
  })

  const learned_features_props = useSelector((store_state) => {
    return FeaturesSelector(store_state, {
      is_clicked: state.is_learned_features_clicked,
      features: learned_features
    })
  })

  return (
    <Card>
      <CardContent>
        <Grid container spacing={1}>
          <CardHeading name={name} />

          <CardNameValuePairBrief name='job' value={job} />
          <CardNameValuePairBrief name='age' value={age} />
          <CardNameValuePairBrief name='gender' value={gender} />
          <CardNameValuePairBrief name='alignment' value={alignment} />
          <CardNameValuePairBrief name='level' value={level} />
          <CardNameValuePairBrief name='sub_level' value={sub_level} />
          <CardNameValuePairBrief name='max_hp' value={max_hp} />
          <CardNameValuePairBrief name='hit_die' value={hit_die} />
          <CardNameValuePairBrief name='spell_slots' value={spell_slots} />

          <CardNameValuePairDynamic
            name='learned_features' value={learned_features} card_type={FeatureStatic} elem_props={learned_features_props} is_vertical
            is_clicked={() => { return state.is_learned_features_clicked }}
            on_click={() => { setState({ ...state, is_learned_features_clicked: !state.is_learned_features_clicked }) }} />

          <CardNameValuePairBrief name='learned_spells' value={learned_spells} is_vertical />

          <CardNameValuePairBrief name='ability_score' value={AbilityScore(ability_score)} />
          <CardNameValuePairBrief name='skill_proficiency' value={SkillProficiencies(skills)} />

          <CardDivider light />
          <CardNameValuePairBrief name='bio' value={bio} />
        </Grid>
      </CardContent>
    </Card >
  )
}

Character.propTypes = {
  name: PropTypes.string.isRequired,
  job: PropTypes.string.isRequired,
  age: PropTypes.number.isRequired,
  gender: PropTypes.string.isRequired,
  alignment: PropTypes.string.isRequired,
  level: PropTypes.number.isRequired,
  sub_level: PropTypes.number.isRequired,
  bio: PropTypes.string.isRequired,
  ability_score: PropTypes.object.isRequired,
  skills: PropTypes.object.isRequired,
  max_hp: PropTypes.number.isRequired,
  hit_die: PropTypes.number.isRequired,
  learned_features: PropTypes.arrayOf(PropTypes.string).isRequired,
  learned_spells: PropTypes.arrayOf(PropTypes.string).isRequired,
  spell_slots: PropTypes.arrayOf(PropTypes.number).isRequired
}

export {
  Character
}
