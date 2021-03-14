import React from 'react'
import { useSelector } from 'react-redux'
import { Grid } from '@material-ui/core'
import LibraryAccordian from 'components/utils/LibraryAccordian'
// import EffectsDisplay from 'components/Effect/EffectsDisplay'
// import FeaturesDisplay from 'components/Feature/FeaturesDisplay'
// import JobsDisplay from 'components/Jobs/JobsDisplay'
import { Effect } from 'components/cards/Effect'
import { Feature } from 'components/cards/Feature'
import Job from 'components/cards/Job'
import { Option } from 'components/cards/Option'
import { NPC } from 'components/cards/NPC'
import { LibraryUpdater } from 'components/utils/LibraryUpdater'

const LibraryPage = () => {
  const { effects } = useSelector((state) => { return state.effects_slice })
  const { features } = useSelector((state) => { return state.features_slice })
  const { jobs } = useSelector((state) => { return state.jobs_slice })
  const { options } = useSelector((state) => { return state.options_slice })
  const { npcs } = useSelector((state) => { return state.npcs_slice })

  return (
    <Grid container>
      <Grid item xs={2} />
      <Grid item xs={8}>
        <Grid container>
          <LibraryAccordian name='Effects' display_object={Effect} elements={effects} />
          <LibraryAccordian name='Features' display_object={Feature} elements={features} />
          <LibraryAccordian name='Options' display_object={Option} elements={options} />
          <LibraryAccordian name='Jobs' display_object={Job} elements={jobs} />
          <LibraryAccordian name='NPCs' display_object={NPC} elements={npcs} />
        </Grid >
      </Grid>
      <Grid item xs={2} />
      <LibraryUpdater address='localhost' port={8080} />
    </Grid>
  )
}

export default LibraryPage
