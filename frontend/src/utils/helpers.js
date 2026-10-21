// Utility helpers

export const fmt = {
  currency: (n, currency = '₹') =>
    `${currency}${Number(n || 0).toLocaleString('en-IN')}`,

  number: (n) => Number(n || 0).toLocaleString('en-IN'),

  pct: (n, decimals = 1) => `${Number(n || 0).toFixed(decimals)}%`,

  date: (d, opts = {}) =>
    new Date(d).toLocaleDateString('en-IN', {
      day: '2-digit', month: 'short', year: 'numeric', ...opts
    }),

  time: (d) =>
    new Date(d).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }),

  datetime: (d) =>
    new Date(d).toLocaleString('en-IN', {
      day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit'
    }),

  duration: (mins) => {
    if (!mins) return '—'
    if (mins < 60) return `${mins}m`
    return `${Math.floor(mins / 60)}h ${mins % 60}m`
  },

  initials: (name = '') =>
    name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2),

  relativeTime: (date) => {
    const diff = Date.now() - new Date(date).getTime()
    const mins = Math.floor(diff / 60000)
    if (mins < 1)  return 'just now'
    if (mins < 60) return `${mins}m ago`
    const hrs = Math.floor(mins / 60)
    if (hrs < 24)  return `${hrs}h ago`
    return `${Math.floor(hrs / 24)}d ago`
  },
}

export const statusColor = {
  active:    'green',
  expired:   'red',
  paused:    'orange',
  cancelled: 'gray',
  paid:      'green',
  pending:   'orange',
  failed:    'red',
  confirmed: 'green',
  scheduled: 'blue',
  completed: 'gray',
}

export const avatarGradients = [
  'linear-gradient(135deg,#3b82f6,#06b6d4)',
  'linear-gradient(135deg,#8b5cf6,#ec4899)',
  'linear-gradient(135deg,#10b981,#06b6d4)',
  'linear-gradient(135deg,#f59e0b,#ef4444)',
  'linear-gradient(135deg,#f97316,#eab308)',
  'linear-gradient(135deg,#ec4899,#8b5cf6)',
  'linear-gradient(135deg,#06b6d4,#3b82f6)',
  'linear-gradient(135deg,#34d399,#10b981)',
]

export const randomGradient = () =>
  avatarGradients[Math.floor(Math.random() * avatarGradients.length)]

export const clsx = (...classes) => classes.filter(Boolean).join(' ')

export const PLAN_COLORS = {
  Basic: '#64748b',
  Pro:   '#3b82f6',
  Elite: '#f59e0b',
}

export const GOAL_ICONS = {
  'Weight Loss':    '🔥',
  'Muscle Gain':    '💪',
  'Endurance':      '🏃',
  'Flexibility':    '🧘',
  'General Fitness':'⚡',
}
