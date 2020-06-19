import {useState} from 'react'
import {useQuery} from '@apollo/react-hooks'
import {gql} from '@apollo/client'
import * as R from 'ramda'

export default function usePlotsQuery() {
  const [plots, setPlots] = useState(null)
  useQuery(gql`
    scatter(vis: "TSNE", group: "Seurat_Clusters_Resolution1", runID: "5eda76def93f82004f4114c6") {
      data {
        name
        mode
        text
        x
        y
        marker {
          color
        }
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