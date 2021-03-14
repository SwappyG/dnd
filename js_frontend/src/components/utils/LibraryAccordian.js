import React from 'react'
import PropTypes from 'prop-types'
import {
  Grid,
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Typography,
  Divider
} from '@material-ui/core'
import ExpandMoreIcon from '@material-ui/icons/ExpandMore'

const LibAccordianSummary = ({ name }) => {
  return (
    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
      <Typography variant='h6'>{name}</Typography>
    </AccordionSummary>
  )
}

const LibAccordianDetail = ({ display_object, elements }) => {
  return (
    <AccordionDetails>
      <Grid container spacing={2}>
        <Grid xs={12}>
          <Divider />
        </Grid>
        {
          elements.map((elem) => {
            return (
              <Grid item xs={12} key={elem.name}>
                {display_object(elem)}
              </Grid>
            )
          })
        }
      </Grid>
    </AccordionDetails>
  )
}

const LibraryAccordian = ({ name, display_object, elements }) => {
  return (
    <Grid xs={12} >
      <Accordion>
        <LibAccordianSummary name={name} />
        <LibAccordianDetail display_object={display_object} elements={elements} />
      </Accordion>
    </Grid>
  )
}

LibAccordianSummary.propTypes = {
  name: PropTypes.string.isRequired
}

LibAccordianDetail.propTypes = {
  display_object: PropTypes.func.isRequired,
  elements: PropTypes.arrayOf(PropTypes.object).isRequired
}

LibraryAccordian.propTypes = {
  name: PropTypes.string.isRequired,
  display_object: PropTypes.func.isRequired,
  elements: PropTypes.arrayOf(PropTypes.object).isRequired
}

export {
  LibAccordianDetail,
  LibAccordianSummary
}

export default LibraryAccordian
