import { useState } from 'react'
import { Search } from 'lucide-react'
import { supabase } from '../supabase'
import ClientCard from '../components/ClientCard'

const mockClients = [
  { id: '1', name: 'TechnoSmart', lastAccess: new Date(2026, 2, 21, 14, 30), pendingTasks: 3, platform: 'Instagram' },
  { id: '2', name: 'Café Delicias', lastAccess: new Date(2026, 2, 22, 9, 15), pendingTasks: 0, platform: 'Facebook' },
  { id: '3', name: 'Fitness Pro', lastAccess: new Date(2026, 2, 20, 16, 45), pendingTasks: 5, platform: 'TikTok' },
  { id: '4', name: 'Moda Elegante', lastAccess: new Date(2026, 2, 22, 11, 0), pendingTasks: 1, platform: 'Instagram' },
  { id: '5', name: 'Restaurante El Buen Sabor', lastAccess: new Date(2026, 2, 19, 13, 20), pendingTasks: 2, platform: 'Facebook' },
  { id: '6', name: 'Librería Cultural', lastAccess: new Date(2026, 2, 22, 8, 30), pendingTasks: 0, platform: 'Twitter' },
  { id: '7', name: 'AutoParts Express', lastAccess: new Date(2026, 2, 21, 10, 0), pendingTasks: 4, platform: 'LinkedIn' },
  { id: '8', name: 'Belleza Natural Spa', lastAccess: new Date(2026, 2, 22, 15, 45), pendingTasks: 0, platform: 'Instagram' },
  { id: '9', name: 'Inmobiliaria Premium', lastAccess: new Date(2026, 2, 18, 12, 0), pendingTasks: 6, platform: 'Facebook' },
]

function Clients() {
  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState('alphabetical')
  const [selectedClient, setSelectedClient] = useState(null)

  useEffect(() => {
    let uuid = await supabase.auth.getUser()?.id
    if (uuid) {
      const { data: { clients } } = await supabase.from('clients').select('*').eq('user_id', uuid)
      mapClients(clients)
      // Aquí deberías mapear los datos de tu base de datos al formato que espera tu componente
      // setClients(clients.map(c => ({ id: c.id, name: c.name, lastAccess: new Date(c.last_access), pendingTasks: c.pending_tasks, platform: c.platform })))
    }
    }, [])

  const getSortedClients = () => {
    let filtered = mockClients.filter(c =>
      c.name.toLowerCase().includes(search.toLowerCase())
    )
    switch (sortBy) {
      case 'alphabetical':
        return [...filtered].sort((a, b) => a.name.localeCompare(b.name))
      case 'lastAccess':
        return [...filtered].sort((a, b) => b.lastAccess - a.lastAccess)
      case 'pendingTasks':
        return [...filtered].sort((a, b) => b.pendingTasks - a.pendingTasks)
      default:
        return filtered
    }
  }

  const clients = getSortedClients()

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Clients</h1>
        <p className="text-gray-500 mt-1">Orchestrate and organise all your clients in one place</p>
      </div>

      {/* Búsqueda y orden */}
      <div className="flex items-center gap-4 mb-6 bg-white border border-gray-200 rounded-xl p-3">
        <div className="flex items-center gap-2 flex-1">
          <Search className="w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search clients..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="flex-1 outline-none text-sm text-gray-700 placeholder-gray-400"
          />
        </div>
        <select
          value={sortBy}
          onChange={e => setSortBy(e.target.value)}
          className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 outline-none text-gray-700"
        >
          <option value="alphabetical">Alphabetical</option>
          <option value="lastAccess">Last accessed</option>
          <option value="pendingTasks">Pending tasks</option>
        </select>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-white border border-gray-200 rounded-xl p-4">
          <p className="text-sm text-gray-500">Total clients</p>
          <p className="text-2xl font-bold mt-1">{clients.length}</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-xl p-4">
          <p className="text-sm text-gray-500">With pending tasks</p>
          <p className="text-2xl font-bold mt-1 text-amber-500">
            {clients.filter(c => c.pendingTasks > 0).length}
          </p>
        </div>
        <div className="bg-white border border-gray-200 rounded-xl p-4">
          <p className="text-sm text-gray-500">Total tasks</p>
          <p className="text-2xl font-bold mt-1 text-primary">
            {clients.reduce((sum, c) => sum + c.pendingTasks, 0)}
          </p>
        </div>
      </div>

      {/* Grid */}
      {clients.length > 0 ? (
        <div className="grid grid-cols-3 gap-4">
          {clients.map(client => (
            <ClientCard
              key={client.id}
              client={client}
              onClick={() => console.log('Client clicked:', client.id)}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
          <p className="text-gray-400">No clients found</p>
        </div>
      )}
    </div>
  )
}

export default Clients