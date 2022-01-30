import { configureStore } from '@reduxjs/toolkit'
import logger from 'redux-logger'

import root from './root'

const store = configureStore({
  reducer: root,
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware({
      immutableCheck: {}
    }).concat([logger])
})

export default store
