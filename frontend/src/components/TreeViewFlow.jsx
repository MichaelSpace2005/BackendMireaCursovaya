import React, { useEffect, useState, useCallback } from 'react'
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  MiniMap,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  NodeTypes,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { useStore } from '../store'

const MechanicNode = ({ data }) => (
  <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-blue-500 min-w-fit">
    <div className="flex">
      <div>
        <div className="font-bold text-sm text-gray-800">{data.label}</div>
        <div className="text-xs text-gray-600">{data.description}</div>
        <div className="text-xs text-gray-500 mt-1">Year: {data.year}</div>
      </div>
    </div>
  </div>
)

const nodeTypes = {
  mechanicNode: MechanicNode,
}

export default function TreeViewFlow() {
  const { selectedMechanic, fetchMechanicTree } = useStore()
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [treeData, setTreeData] = useState(null)

  useEffect(() => {
    if (selectedMechanic) {
      loadTree(selectedMechanic.id)
    }
  }, [selectedMechanic])

  const loadTree = async (mechanicId) => {
    const tree = await fetchMechanicTree(mechanicId)
    setTreeData(tree)
    buildNodesAndEdges(tree)
  }

  const buildNodesAndEdges = (treeData) => {
    const newNodes = []
    const newEdges = []
    let nodeId = 0
    const positionMap = {}
    const levelWidth = 250

    const traverse = (node, x, y, level) => {
      const currentId = `node-${nodeId++}`
      positionMap[node.id] = currentId

      newNodes.push({
        id: currentId,
        data: {
          label: node.name,
          description: node.description,
          year: node.year,
        },
        position: { x, y },
        type: 'mechanicNode',
      })

      if (node.children && node.children.length > 0) {
        const childWidth = node.children.length * levelWidth
        const startX = x - childWidth / 2 + levelWidth / 2

        node.children.forEach((child, index) => {
          const childX = startX + index * levelWidth
          const childY = y + 150

          const childId = traverse(child, childX, childY, level + 1)

          newEdges.push({
            id: `edge-${currentId}-${childId}`,
            source: currentId,
            target: childId,
            animated: true,
            label: 'evolves to',
          })
        })
      }

      return currentId
    }

    if (treeData) {
      traverse(treeData, 0, 0, 0)
    }

    setNodes(newNodes)
    setEdges(newEdges)
  }

  const onConnect = useCallback((connection) => {
    setEdges((eds) => addEdge(connection, eds))
  }, [setEdges])

  return (
    <div className="bg-gray-800 rounded-lg p-6 shadow-lg h-screen">
      <h2 className="text-2xl font-bold text-white mb-4 absolute top-8 left-8 z-10">
        Interactive Evolution Tree
      </h2>
      {selectedMechanic ? (
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
        >
          <Background />
          <Controls />
          <MiniMap />
        </ReactFlow>
      ) : (
        <div className="text-gray-400 text-center py-12">
          Select a mechanic from the list to view its evolution tree
        </div>
      )}
    </div>
  )
}
