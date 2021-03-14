import React from 'react'
import PropTypes from 'prop-types'
import { Grid, Box, FormControl, InputLabel, Input, TextField, Typography } from '@material-ui/core'
// import { handle_change, handle_click } from 'components/utils/ElementEdit'

// const full_row = (html_data) => {
//   return (
//     <Grid item xs={12}>
//       {html_data}
//     </Grid>
//   )
// }

const InputTextRow = ({ input_label, input_value, on_change_handler }) => {
  return (
    <Grid item xs={12}>
      <FormControl fullWidth>
        <InputLabel>{input_label}</InputLabel>
        <Input value={input_value} onChange={on_change_handler} />
      </FormControl>
    </Grid>
  )
}

InputTextRow.propTypes = {
  input_label: PropTypes.string.isRequired,
  input_value: PropTypes.string.isRequired,
  on_change_handler: PropTypes.any
}

const InputTextField = ({ text_field_value, num_rows, on_change_handler }) => {
  return (
    <Grid item xs={12}>
      <FormControl fullWidth>
        <TextField multiline rows={num_rows} defaultValue={text_field_value} onChange={on_change_handler} />
      </FormControl>
    </Grid>
  )
}

InputTextField.propTypes = {
  text_field_value: PropTypes.string.isRequired,
  num_rows: PropTypes.number.isRequired,
  on_change_handler: PropTypes.any
}

const ClickableTypography = ({ on_click_cb, options, body }) => {
  return (
    <Grid container>
      <Grid item xs={12}>
        <Typography onClick={on_click_cb} {...options}>
          {body}
        </Typography>
      </Grid>
    </Grid >
  )
}

ClickableTypography.propTypes = {
  on_click_cb: PropTypes.any.isRequired,
  options: PropTypes.object.isRequired,
  body: PropTypes.element.isRequired
}

const ClickableNameValuePair = ({ name, value, on_click_cb, typography_opts }) => {
  if (Array.isArray(value)) {
    value = `[${value.join(', ')}]`
  }

  const box = (
    <Box fontWeight="fontWeightBold">{name}:</Box>
  )

  const body = (
    <Grid container>
      <Grid item xs={2}>{box}</Grid>
      <Grid item xs={10}>{value}</Grid>
    </Grid>
  )

  return (
    <ClickableTypography
      on_click_cb={() => { on_click_cb({ name: name, value: value }) }}
      options={typography_opts}
      body={body}
    />
  )
}

ClickableNameValuePair.propTypes = {
  name: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  on_click_cb: PropTypes.any.isRequired,
  typography_opts: PropTypes.object.isRequired
}

// const edittable_typography = (state, state_setter, field_name, field_value, field_value_formatter, typography_options) => {
//   return (
//     <Grid item xs={12}>
//       <Typography
//         {...typography_options}
//         onClick={() => { handle_click(state, state_setter, field_name, field_value) }}
//       >
//         {field_value_formatter({ name: field_name, value: field_value })}
//       </Typography>
//     </Grid>
//   )
// }

// const get_input_text_by_type = (state, state_setter, input_type, field_name, field_value) => {
//   const input_event_handler = (event) => handle_change(state, state_setter, { editted_value: event.target.value })
//   if (input_type === 'input') {
//     return InputTextRow(field_name, state.editted_value, input_event_handler)
//   } else if (input_type === 'text_area') {
//     return InputTextField(state.editted_value, 4, input_event_handler)
//   }
// }

// const typography_or_input_type = (state, state_setter, props, field_name, input_type, field_value_formatter, typography_options) => {
//   const field_value = props[field_name] || 'None'
//   if ((state.field_under_edit === null) || (state.field_under_edit !== field_name)) {
//     return edittable_typography(state, state_setter, field_name, field_value, field_value_formatter, typography_options)
//   }
//   if (state.editted_value === null) {
//     state_setter({ ...state, editted_value: field_value })
//   }
//   return get_input_text_by_type(state, state_setter, input_type, field_name, field_value)
// }

export {
  ClickableNameValuePair
}
