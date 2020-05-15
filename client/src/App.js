import React from 'react';
import './App.css';
import 'semantic-ui-css/semantic.min.css';
import {Grid, Segment, Menu} from 'semantic-ui-react'

import {ApolloProvider} from '@apollo/react-hooks'

import {ApolloClient, HttpLink, InMemoryCache} from '@apollo/client'

import {usePlotsQuery} from './hooks'
import * as R from 'ramda'

const client = new ApolloClient({
  cache: new InMemoryCache(),
  link: new HttpLink({
    uri: 'http://localhost:8000' //should use env
  })
})

function App() {
  const plots = usePlotsQuery()
  if (R.isNil(plots)) {
    return null
  }
  return (
    <Grid as={Segment} basic style={{height: '80vh'}}>
      <Grid.Column width={10}>
        <Segment style={{height: '100%'}}>
        </Segment>
      </Grid.Column>
      <Grid.Column width={6}>
        <Segment>
          <Menu vertical>
          {
            R.map(
              ({plotType}) => <Menu.Item key={plotType} content={plotType} />,
              plots
            )
          }
          </Menu>
        </Segment>
      </Grid.Column>
    </Grid>
  );
}

export default App;
