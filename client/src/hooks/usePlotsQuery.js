import {useState} from 'react'
import {useQuery} from '@apollo/react-hooks'
import {gql} from '@apollo/client'
import * as R from 'ramda'

export default function usePlotsQuery() {
  const [plots, setPlots] = useState(null)
  useQuery(gql`
    query {
      plots {
        plotType
      }
    }
  `, {
    onCompleted: ({plots}) => {
      if (R.not(R.isNil(plots))) {
        setPlots(plots)
      }
    }
  })

  return plots
}