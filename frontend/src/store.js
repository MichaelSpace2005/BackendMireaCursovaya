import { create } from 'zustand'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const useStore = create((set, get) => ({
  // State
  mechanics: [],
  links: [],
  selectedMechanic: null,
  isLoading: false,
  error: null,

  // Actions
  setMechanics: (mechanics) => set({ mechanics }),
  setLinks: (links) => set({ links }),
  setSelectedMechanic: (mechanic) => set({ selectedMechanic: mechanic }),
  setIsLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),

  // Async actions
  fetchMechanics: async () => {
    try {
      set({ isLoading: true })
      const response = await fetch(`${API_BASE}/api/v1/mechanics/`)
      const data = await response.json()
      set({ mechanics: data, isLoading: false })
    } catch (err) {
      set({ error: err.message, isLoading: false })
    }
  },

  fetchMechanicTree: async (id) => {
    try {
      set({ isLoading: true })
      const response = await fetch(`${API_BASE}/api/v1/mechanics/${id}/tree`)
      const data = await response.json()
      set({ isLoading: false })
      return data
    } catch (err) {
      set({ error: err.message, isLoading: false })
      return null
    }
  },

  fetchLinks: async () => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/mechanics/links`)
      const data = await response.json()
      set({ links: data })
    } catch (err) {
      set({ error: err.message })
    }
  },

  createMechanic: async (name, description, year) => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/mechanics/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, description, year })
      })
      if (!response.ok) throw new Error('Failed to create mechanic')
      const newMechanic = await response.json()
      set({ mechanics: [...get().mechanics, newMechanic] })
      return newMechanic
    } catch (err) {
      set({ error: err.message })
      return null
    }
  },

  createLink: async (fromId, toId, linkType = 'evolves_to') => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/mechanics/links`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          from_id: fromId,
          to_id: toId,
          type: linkType
        })
      })
      if (!response.ok) throw new Error('Failed to create link')
      const newLink = await response.json()
      set({ links: [...get().links, newLink] })
      return newLink
    } catch (err) {
      set({ error: err.message })
      return null
    }
  },
}))
