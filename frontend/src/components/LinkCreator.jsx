import React, { useState } from 'react'
import { useStore } from '../store'

export default function LinkCreator() {
  const { mechanics, selectedMechanic, createLink } = useStore()
  const [targetMechanic, setTargetMechanic] = useState(null)
  const [linkType, setLinkType] = useState('evolves_to')
  const [isLoading, setIsLoading] = useState(false)

  const handleCreateLink = async () => {
    if (!selectedMechanic || !targetMechanic) return

    setIsLoading(true)
    await createLink(selectedMechanic.id, targetMechanic.id, linkType)
    setTargetMechanic(null)
    setIsLoading(false)
  }

  return (
    <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-white mb-4">Create Link</h2>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">From Mechanic</label>
          <div className="px-4 py-2 bg-gray-700 rounded-lg text-blue-300">
            {selectedMechanic?.name || 'Select a mechanic'}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Link Type</label>
          <select
            value={linkType}
            onChange={(e) => setLinkType(e.target.value)}
            className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
          >
            <option value="evolves_to">Evolves To</option>
            <option value="extends">Extends</option>
            <option value="replaces">Replaces</option>
            <option value="combines_with">Combines With</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">To Mechanic</label>
          <select
            value={targetMechanic?.id || ''}
            onChange={(e) => {
              const mechanic = mechanics.find(m => m.id === parseInt(e.target.value))
              setTargetMechanic(mechanic)
            }}
            className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
          >
            <option value="">Select target mechanic</option>
            {mechanics
              .filter(m => !selectedMechanic || m.id !== selectedMechanic.id)
              .map(mechanic => (
                <option key={mechanic.id} value={mechanic.id}>
                  {mechanic.name}
                </option>
              ))}
          </select>
        </div>

        <button
          onClick={handleCreateLink}
          disabled={!selectedMechanic || !targetMechanic || isLoading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors font-medium"
        >
          {isLoading ? 'Creating...' : 'Create Link'}
        </button>
      </div>
    </div>
  )
}
