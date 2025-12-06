import React, { useEffect, useState, useRef } from 'react'
import { useStore } from '../store'

export default function TreeView() {
  const { mechanics, links, selectedMechanic, fetchMechanicTree } = useStore()
  const [treeData, setTreeData] = useState(null)
  const canvasRef = useRef(null)
  const [connecting, setConnecting] = useState(null)

  useEffect(() => {
    if (selectedMechanic) {
      loadTree(selectedMechanic.id)
    }
  }, [selectedMechanic])

  const loadTree = async (mechanicId) => {
    const tree = await fetchMechanicTree(mechanicId)
    setTreeData(tree)
    drawTree()
  }

  const drawTree = () => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    if (!treeData) return

    const nodeWidth = 180
    const nodeHeight = 80
    const verticalGap = 140
    const horizontalGap = 200

    const drawNode = (node, x, y, depth = 0) => {
      const m = node?.mechanic || node
      if (!m) return
      // Card background
      ctx.beginPath()
      ctx.roundRect(x - nodeWidth / 2, y - nodeHeight / 2, nodeWidth, nodeHeight, 12)
      ctx.fillStyle = '#1f2937'
      ctx.fill()
      ctx.strokeStyle = '#60a5fa'
      ctx.lineWidth = 2
      ctx.stroke()

      // Text
      ctx.fillStyle = '#e5e7eb'
      ctx.font = 'bold 14px Arial'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      const title = (m.name || '').slice(0, 20)
      ctx.fillText(title, x, y - 10)

      ctx.font = '12px Arial'
      ctx.fillStyle = '#9ca3af'
      const desc = (m.description || '').slice(0, 24)
      ctx.fillText(desc, x, y + 10)
    }

    const drawConnections = (node, x, y, visited = new Set()) => {
      const m = node?.mechanic || node
      if (!m || visited.has(m.id)) return
      visited.add(m.id)

      const children = node?.children || []
      if (children.length > 0) {
        const childWidth = children.length * horizontalGap
        const startX = x - childWidth / 2 + horizontalGap / 2

        children.forEach((child, index) => {
          const childX = startX + index * horizontalGap
          const childY = y + verticalGap

          // Draw line
          ctx.beginPath()
          ctx.moveTo(x, y + nodeHeight / 2)
          ctx.lineTo(childX, childY - nodeHeight / 2)
          ctx.strokeStyle = '#60a5fa'
          ctx.lineWidth = 2
          ctx.stroke()

          // Draw arrow
          const angle = Math.atan2(childY - y, childX - x)
          ctx.beginPath()
          ctx.moveTo(childX, childY)
          ctx.lineTo(childX - 10 * Math.cos(angle - Math.PI / 6), childY - 10 * Math.sin(angle - Math.PI / 6))
          ctx.lineTo(childX - 10 * Math.cos(angle + Math.PI / 6), childY - 10 * Math.sin(angle + Math.PI / 6))
          ctx.fill()

          drawNode(child, childX, childY, depth + 1)
          drawConnections(child, childX, childY, visited)
        })
      }
    }

    if (treeData) {
      drawNode(treeData, canvas.width / 2, 70)
      drawConnections(treeData, canvas.width / 2, 70)
    }
  }

  return (
    <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-white mb-4">Evolution Tree</h2>
      {selectedMechanic ? (
        <div>
          <div className="mb-4 p-4 bg-gray-700 rounded-lg">
            <h3 className="text-xl font-bold text-blue-400">{selectedMechanic.name}</h3>
            <p className="text-gray-300">{selectedMechanic.description}</p>
            <p className="text-sm text-gray-400 mt-2">Year: {selectedMechanic.year}</p>
          </div>
          <canvas
            ref={canvasRef}
            width={800}
            height={600}
            className="w-full border-2 border-gray-600 rounded-lg bg-gray-900"
          />
        </div>
      ) : (
        <div className="text-gray-400 text-center py-12">
          Select a mechanic from the list to view its evolution tree
        </div>
      )}
    </div>
  )
}
