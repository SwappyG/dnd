import React from 'react'
import { useSelector } from 'react-redux'
import { Grid } from '@material-ui/core'
import LibraryAccordian from 'components/utils/LibraryAccordian'

import { Effect } from 'components/cards/Effect'
import { Feature } from 'components/cards/Feature'
import { Job } from 'components/cards/Job'
import { Option } from 'components/cards/Option'
import { NPC } from 'components/cards/NPC'
import { Location } from 'components/cards/Location'
import { Weapon } from 'components/cards/Weapon'
import { Item } from 'components/cards/Item'
import { Armor } from 'components/cards/Armor'
import { LibraryUpdater } from 'components/utils/LibraryUpdater'

const LibraryPage = () => {
  const { effects } = useSelector((state) => { return state.effects_slice })
  const { features } = useSelector((state) => { return state.features_slice })
  const { jobs } = useSelector((state) => { return state.jobs_slice })
  const { options } = useSelector((state) => { return state.options_slice })
  const { npcs } = useSelector((state) => { return state.npcs_slice })
  const { locations } = useSelector((state) => { return state.locations_slice })
  const { items } = useSelector((state) => { return state.items_slice })

  const weapons = items.filter((elem) => { return elem.item_type === 'WEAPON' })
  const armor = items.filter((elem) => { return elem.item_type === 'ARMOR' })
  const only_items = items.filter((elem) => { return elem.item_type === 'BASIC' })

  return (
    <Grid container>
      <Grid item xs={2} />
      <Grid item xs={8}>
        <Grid container spacing={2}>
          <LibraryAccordian name='Effects' display_object={Effect} elements={effects} />
          <LibraryAccordian name='Features' display_object={Feature} elements={features} />
          <LibraryAccordian name='Options' display_object={Option} elements={options} />
          <LibraryAccordian name='Jobs' display_object={Job} elements={jobs} />
          <LibraryAccordian name='NPCs' display_object={NPC} elements={npcs} />
          <LibraryAccordian name='Locations' display_object={Location} elements={locations} />
          <LibraryAccordian name='Items' display_object={Item} elements={only_items} />
          <LibraryAccordian name='Armor' display_object={Armor} elements={armor} />
          <LibraryAccordian name='Weapons' display_object={Weapon} elements={weapons} />
        </Grid >
      </Grid>
      <Grid item xs={2} />
      <LibraryUpdater address='localhost' port={8080} />
    </Grid>
  )
}

export default LibraryPage
