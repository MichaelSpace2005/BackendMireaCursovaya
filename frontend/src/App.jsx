import React, { useEffect } from 'react'
import { useStore } from './store'
import MechanicsList from './components/MechanicsList'
import TreeView from './components/TreeView'
import LinkCreator from './components/LinkCreator'

export default function App() {
  const { fetchMechanics, fetchLinks } = useStore()

  useEffect(() => {
    fetchMechanics()
    fetchLinks()
  }, [])

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-900 to-blue-700 p-6 shadow-lg">
        <h1 className="text-4xl font-bold">Evolution Tree of Game Mechanics</h1>
        <p className="text-blue-200 mt-2">Interactive drag-n-drop visualization</p>
      </header>

      {/* Main Content */}
      <main className="container mx-auto p-6">
        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Left Column - List */}
          <div>
            <MechanicsList />
          </div>

          {/* Center Column - Tree */}
          <div className="lg:col-span-2">
            <TreeView />
          </div>
        </div>

        {/* Link Creator */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <LinkCreator />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 p-6 mt-12 text-center text-gray-400">
        <p>Evolution Tree Backend - Coursework Project</p>
        <p className="text-sm mt-2">Built with FastAPI, SQLAlchemy, React & Tailwind CSS</p>
      </footer>
    </div>
  )
}
