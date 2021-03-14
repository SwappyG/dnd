import React from 'react'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import LibraryPage from 'pages/LibraryPage'

const App = () => {
  return (
    <Router>
      <Switch>
        <Route exact path='/' component={LibraryPage} />
      </Switch>
    </Router>
  )
}

export default App
