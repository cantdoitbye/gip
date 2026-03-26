import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { lazy, Suspense, useEffect, useState } from 'react'
import { ROUTES } from './types/routes'
import Layout from './components/layout/Layout'
import ProtectedRoute from './components/auth/ProtectedRoute'
import { useAuthStore } from './store/authStore'

const Login = lazy(() => import('./pages/Login'))
const Register = lazy(() => import('./pages/Register'))
const ForgotPassword = lazy(() => import('./pages/ForgotPassword'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Profile = lazy(() => import('./pages/Profile'))
const Traffic = lazy(() => import('./pages/Traffic'))
const Forecasting = lazy(() => import('./pages/Forecasting'))
const Simulation = lazy(() => import('./pages/Simulation'))
const Sites = lazy(() => import('./pages/Sites'))
const Monitoring = lazy(() => import('./pages/Monitoring'))
const Reports = lazy(() => import('./pages/Reports'))
const AiAssistant = lazy(() => import('./pages/AiAssistant'))
const Admin = lazy(() => import('./pages/Admin'))
const UserManagement = lazy(() => import('./pages/UserManagement'))

function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>
  )
}

function App() {
  const { initializeAuth } = useAuthStore()
  const [isInitializing, setIsInitializing] = useState(true)

  useEffect(() => {
    initializeAuth().finally(() => {
      setIsInitializing(false)
    })
  }, [initializeAuth])

  if (isInitializing) {
    return <LoadingSpinner />
  }

  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path={ROUTES.HOME} element={<Navigate to={ROUTES.DASHBOARD} replace />} />
          <Route path={ROUTES.LOGIN} element={<Login />} />
          <Route path={ROUTES.REGISTER} element={<Register />} />
          <Route path={ROUTES.FORGOT_PASSWORD} element={<ForgotPassword />} />
          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route path={ROUTES.DASHBOARD} element={<Dashboard />} />
              <Route path={ROUTES.PROFILE} element={<Profile />} />
              <Route path={ROUTES.TRAFFIC} element={<Traffic />} />
              <Route path={ROUTES.FORECASTING} element={<Forecasting />} />
              <Route path={ROUTES.SIMULATION} element={<Simulation />} />
              <Route path={ROUTES.SITES} element={<Sites />} />
              <Route path={ROUTES.MONITORING} element={<Monitoring />} />
              <Route path={ROUTES.REPORTS} element={<Reports />} />
              <Route path={ROUTES.AI_ASSISTANT} element={<AiAssistant />} />
              <Route path={ROUTES.ADMIN} element={<Admin />} />
              <Route path={ROUTES.USER_MANAGEMENT} element={<UserManagement />} />
            </Route>
          </Route>
          <Route path="*" element={<Navigate to={ROUTES.DASHBOARD} replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

export default App
