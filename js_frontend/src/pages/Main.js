import React, { useState } from 'react'
import Tab from '@material-ui/core/Tab'
import Tabs from '@material-ui/core/Tabs'
import Paper from '@material-ui/core/Paper'
import { Library } from 'components/library/Library'
import { LibraryUpdater } from 'components/library/LibraryUpdater'

const Main = () => {
  const [value, set_value] = useState(0)

  return (
    <>
      <Paper square>
        <Tabs
          centered
          variant="fullWidth"
          indicatorColor='primary'
          textColor='primary'
          value={value}
          onChange={(event, index) => { set_value(index) }}
        >
          <Tab label="Game" id='simple-tab-0' aria-controls='tab-0' />
          <Tab label="Library" id='simple-tab-1' aria-controls='tab-1' />
        </Tabs>
        {value === 1 && (<Library />)}
      </Paper>
      <LibraryUpdater address='localhost' port={8080} />
    </>
  )
}

export {
  Main
}
