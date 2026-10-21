import { useState, useEffect, useCallback, useRef } from 'react'

/**
 * useApi — Generic data fetching hook
 * @param {Function} apiCall - function that returns a Promise (axios call)
 * @param {*[]} deps - dependency array to re-fetch
 * @param {Object} opts - { immediate: bool, transform: fn }
 */
export function useApi(apiCall, deps = [], opts = {}) {
  const { immediate = true, transform = d => d } = opts
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(immediate)
  const [error, setError]     = useState(null)
  const mountedRef = useRef(true)

  const execute = useCallback(async (...args) => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiCall(...args)
      const payload = res?.data !== undefined ? res.data : res
      if (mountedRef.current) setData(transform(payload))
      return payload
    } catch (err) {
      if (mountedRef.current) setError(err.message || 'Something went wrong')
      throw err
    } finally {
      if (mountedRef.current) setLoading(false)
    }
  }, deps) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    mountedRef.current = true
    if (immediate) execute()
    return () => { mountedRef.current = false }
  }, [execute, immediate])

  const refresh = () => execute()
  return { data, loading, error, execute, refresh }
}

/**
 * useDebounce — debounce a value
 */
export function useDebounce(value, delay = 400) {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(t)
  }, [value, delay])
  return debounced
}

/**
 * useCountUp — animates a number from 0 → target
 */
export function useCountUp(target, duration = 1800) {
  const [count, setCount] = useState(0)
  useEffect(() => {
    if (!target) return
    const start = performance.now()
    const step = (now) => {
      const elapsed = now - start
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 4)
      setCount(Math.floor(eased * target))
      if (progress < 1) requestAnimationFrame(step)
      else setCount(target)
    }
    requestAnimationFrame(step)
  }, [target, duration])
  return count
}

/**
 * useLocalStorage — synced localStorage state
 */
export function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch { return initialValue }
  })
  const set = useCallback(v => {
    setValue(v)
    try { window.localStorage.setItem(key, JSON.stringify(v)) } catch {}
  }, [key])
  return [value, set]
}
