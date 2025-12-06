import React, { useState, useCallback } from 'react'
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd'
import { useStore } from '../store'

export default function MechanicsList() {
  const { mechanics, selectedMechanic, setSelectedMechanic, createMechanic } = useStore()
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ name: '', description: '', year: new Date().getFullYear() })

  const handleAddMechanic = async (e) => {
    e.preventDefault()
    if (formData.name.trim()) {
      await createMechanic(formData.name, formData.description, formData.year)
      setFormData({ name: '', description: '', year: new Date().getFullYear() })
      setShowForm(false)
    }
  }

  const onDragEnd = (result) => {
    const { source, destination, draggableId } = result
    if (!destination) return

    // Handle drag-n-drop reordering here if needed
    console.log(`Dragged ${draggableId} from ${source.index} to ${destination.index}`)
  }

  return (
    <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">Game Mechanics</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          + Add Mechanic
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleAddMechanic} className="mb-6 p-4 bg-gray-700 rounded-lg">
          <input
            type="text"
            placeholder="Mechanic name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="w-full px-4 py-2 mb-3 bg-gray-600 text-white rounded-lg border border-gray-500 focus:border-blue-500 focus:outline-none"
            required
          />
          <textarea
            placeholder="Description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="w-full px-4 py-2 mb-3 bg-gray-600 text-white rounded-lg border border-gray-500 focus:border-blue-500 focus:outline-none"
            rows="3"
          />
          <input
            type="number"
            placeholder="Year"
            value={formData.year}
            onChange={(e) => setFormData({ ...formData, year: parseInt(e.target.value) })}
            className="w-full px-4 py-2 mb-3 bg-gray-600 text-white rounded-lg border border-gray-500 focus:border-blue-500 focus:outline-none"
          />
          <div className="flex gap-2">
            <button type="submit" className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
              Save
            </button>
            <button
              type="button"
              onClick={() => setShowForm(false)}
              className="flex-1 bg-gray-600 hover:bg-gray-500 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      <DragDropContext onDragEnd={onDragEnd}>
        <Droppable droppableId="mechanics-list">
          {(provided, snapshot) => (
            <div
              {...provided.droppableProps}
              ref={provided.innerRef}
              className="space-y-2 max-h-96 overflow-y-auto"
            >
              {mechanics.length === 0 ? (
                <div className="text-gray-400 text-center py-8">No mechanics yet. Create one to start!</div>
              ) : (
                mechanics.map((mechanic, index) => (
                  <Draggable key={mechanic.id} draggableId={String(mechanic.id)} index={index}>
                    {(provided, snapshot) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        onClick={() => setSelectedMechanic(mechanic)}
                        className={`mechanism-card ${
                          selectedMechanic?.id === mechanic.id ? 'selected' : ''
                        } ${snapshot.isDragging ? 'dragging' : ''}`}
                      >
                        <div className="font-bold text-lg">{mechanic.name}</div>
                        <div className="text-sm text-blue-200">{mechanic.description}</div>
                        <div className="text-xs text-blue-100 mt-2">Year: {mechanic.year}</div>
                      </div>
                    )}
                  </Draggable>
                ))
              )}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
    </div>
  )
}
