import { createContext, useContext, useReducer, useCallback } from 'react'

const AppContext = createContext(null)

const initialState = {
  sidebarOpen: true,
  aiPanelOpen: false,
  toasts: [],
  user: { name: 'Admin', role: 'Super Admin', avatar: 'A' },
  theme: 'light',
}

function reducer(state, action) {
  switch (action.type) {
    case 'TOGGLE_SIDEBAR':
      return { ...state, sidebarOpen: !state.sidebarOpen }
    case 'SET_SIDEBAR':
      return { ...state, sidebarOpen: action.payload }
    case 'TOGGLE_AI_PANEL':
      return { ...state, aiPanelOpen: !state.aiPanelOpen }
    case 'SET_AI_PANEL':
      return { ...state, aiPanelOpen: action.payload }
    case 'ADD_TOAST':
      return { ...state, toasts: [...state.toasts, { id: Date.now(), ...action.payload }] }
    case 'REMOVE_TOAST':
      return { ...state, toasts: state.toasts.filter(t => t.id !== action.payload) }
    default:
      return state
  }
}

export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState)

  const toggleSidebar  = useCallback(() => dispatch({ type: 'TOGGLE_SIDEBAR' }), [])
  const setSidebar     = useCallback(v  => dispatch({ type: 'SET_SIDEBAR', payload: v }), [])
  const toggleAiPanel  = useCallback(() => dispatch({ type: 'TOGGLE_AI_PANEL' }), [])
  const setAiPanel     = useCallback(v  => dispatch({ type: 'SET_AI_PANEL', payload: v }), [])

  const addToast = useCallback(({ message, type = 'info', duration = 4000 }) => {
    const id = Date.now()
    dispatch({ type: 'ADD_TOAST', payload: { id, message, type, duration } })
    setTimeout(() => dispatch({ type: 'REMOVE_TOAST', payload: id }), duration)
  }, [])

  const removeToast = useCallback(id => dispatch({ type: 'REMOVE_TOAST', payload: id }), [])

  return (
    <AppContext.Provider value={{
      ...state,
      toggleSidebar, setSidebar,
      toggleAiPanel, setAiPanel,
      addToast, removeToast,
    }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within AppProvider')
  return ctx
}
