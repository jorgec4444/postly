import { Calendar, AlertCircle, CheckCircle2 } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

function ClientCard({ client, onClick }) {
  const hasPendingTasks = client.pendingTasks > 0

  return (
    <div 
      onClick={onClick}
      className="bg-white border border-gray-200 rounded-xl p-4 cursor-pointer hover:shadow-md hover:-translate-y-1 transition-all duration-200"
    >
      {/* Header card */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {/* Avatar con inicial */}
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-semibold text-lg">
            {client.name.charAt(0).toUpperCase()}
          </div>
          <div>
            <p className="font-semibold text-gray-900">{client.name}</p>
            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
              {client.platform}
            </span>
          </div>
        </div>
        {/* Icono estado */}
        {hasPendingTasks 
          ? <AlertCircle className="w-5 h-5 text-amber-500" />
          : <CheckCircle2 className="w-5 h-5 text-green-500" />
        }
      </div>

      {/* Último acceso */}
      <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
        <Calendar className="w-4 h-4" />
        <span>Last access {formatDistanceToNow(client.lastAccess, { addSuffix: true })}</span>
      </div>

      {/* Badge tareas */}
      {hasPendingTasks 
        ? <span className="text-xs bg-red-100 text-red-600 px-3 py-1 rounded-full font-medium">
            {client.pendingTasks} pending tasks
          </span>
        : <span className="text-xs border border-green-500 text-green-600 px-3 py-1 rounded-full">
            No pending tasks
          </span>
      }
    </div>
  )
}

export default ClientCard