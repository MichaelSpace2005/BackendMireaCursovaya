import React, { useState } from 'react'
import { useStore } from '../store'

export default function AuthPanel() {
  const { user, token, login, register, logout, error } = useStore()
  const [showRegister, setShowRegister] = useState(false)
  const [formData, setFormData] = useState({ email: '', username: '', password: '' })
  const [isLoading, setIsLoading] = useState(false)

  const handleLogin = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    await login(formData.email, formData.password)
    setFormData({ email: '', username: '', password: '' })
    setIsLoading(false)
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    await register(formData.email, formData.username, formData.password)
    setFormData({ email: '', username: '', password: '' })
    setShowRegister(false)
    setIsLoading(false)
  }

  if (token && user) {
    return (
      <div className="bg-gray-800 rounded-lg p-4 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-white font-medium">{user.username}</p>
            <p className="text-gray-400 text-sm">{user.email}</p>
          </div>
          <button
            onClick={() => logout()}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Logout
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-white mb-4">
        {showRegister ? 'Register' : 'Login'}
      </h2>

      <form onSubmit={showRegister ? handleRegister : handleLogin} className="space-y-4">
        <input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
          required
        />

        {showRegister && (
          <input
            type="text"
            placeholder="Username"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
            required
          />
        )}

        <input
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
          required
        />

        {error && <p className="text-red-400 text-sm">{error}</p>}

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors font-medium"
        >
          {isLoading ? 'Loading...' : showRegister ? 'Register' : 'Login'}
        </button>
      </form>

      <button
        onClick={() => setShowRegister(!showRegister)}
        className="w-full mt-3 text-blue-400 hover:text-blue-300 text-sm transition-colors"
      >
        {showRegister ? 'Already have account? Login' : "Don't have account? Register"}
      </button>
    </div>
  )
}
