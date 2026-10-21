import axios from 'axios'

const BASE_URL = '/api/v1'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor — add auth token
api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('fs_token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// Response interceptor — normalize errors
api.interceptors.response.use(
  res => res,
  err => {
    const msg = err.response?.data?.detail || err.message || 'Network error'
    return Promise.reject(new Error(msg))
  }
)

// ── Dashboard ──────────────────────────────────────────────────
export const dashboardApi = {
  getKPIs:           () => api.get('/dashboard/kpis'),
  getRevenueTrend:   (months=12) => api.get(`/dashboard/revenue-trend?months=${months}`),
  getAttendanceTrend:(days=7)    => api.get(`/dashboard/attendance-trend?days=${days}`),
  getPlanDistribution:()          => api.get('/dashboard/plan-distribution'),
  getAiInsights:     ()           => api.get('/dashboard/ai-insights'),
}

// ── Members ────────────────────────────────────────────────────
export const membersApi = {
  list:   (params={})         => api.get('/members/', { params }),
  get:    (id)                => api.get(`/members/${id}`),
  create: (data)              => api.post('/members/', data),
  update: (id, data)          => api.patch(`/members/${id}`, data),
  delete: (id)                => api.delete(`/members/${id}`),
}

// ── Trainers ───────────────────────────────────────────────────
export const trainersApi = {
  list:   ()     => api.get('/trainers/'),
  get:    (id)   => api.get(`/trainers/${id}`),
  create: (data) => api.post('/trainers/', data),
}

// ── Attendance ─────────────────────────────────────────────────
export const attendanceApi = {
  today:    ()          => api.get('/attendance/today'),
  stats:    ()          => api.get('/attendance/stats'),
  hourly:   ()          => api.get('/attendance/hourly'),
  checkIn:  (data)      => api.post('/attendance/checkin', data),
  checkOut: (id)        => api.patch(`/attendance/${id}/checkout`),
  history:  (memberId, days=30) => api.get(`/attendance/member/${memberId}/history?days=${days}`),
}

// ── Sessions ───────────────────────────────────────────────────
export const sessionsApi = {
  list:   (date)   => api.get('/sessions/', { params: date ? { date } : {} }),
  create: (data)   => api.post('/sessions/', data),
}

// ── Payments / Revenue ─────────────────────────────────────────
export const revenueApi = {
  summary:      ()           => api.get('/payments/summary'),
  transactions: (limit=20)   => api.get(`/payments/transactions?limit=${limit}`),
  trend:        (months=12)  => api.get(`/payments/trend?months=${months}`),
  create:       (data)       => api.post('/payments/', data),
}

// ── Body Measurements ──────────────────────────────────────────
export const measurementsApi = {
  getMember: (memberId) => api.get(`/measurements/member/${memberId}`),
  log:       (data)     => api.post('/measurements/', data),
}

// ── Workouts ───────────────────────────────────────────────────
export const workoutsApi = {
  getPlan:   (goal, level, days) =>
    api.get('/workouts/plan', { params: { goal, level, days_per_week: days } }),
  getLibrary: (muscle) =>
    api.get('/workouts/exercises', { params: muscle ? { muscle_group: muscle } : {} }),
}

// ── Diet ───────────────────────────────────────────────────────
export const dietApi = {
  today:           (memberId) => api.get(`/diet/member/${memberId}/today`),
  logMeal:         (data)     => api.post('/diet/', data),
  recommendations: (memberId) => api.get(`/diet/recommendations/${memberId}`),
}

// ── Reminders ──────────────────────────────────────────────────
export const remindersApi = {
  list:   ()      => api.get('/reminders/'),
  create: (data)  => api.post('/reminders/', data),
  delete: (id)    => api.delete(`/reminders/${id}`),
}

// ── AI Assistant ───────────────────────────────────────────────
export const aiApi = {
  chat:        (message, context) => api.post('/ai/chat', { message, context }),
  suggestions: ()                 => api.get('/ai/suggestions'),
}

export default api
