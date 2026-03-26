import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useState } from 'react'
import Button from '../components/common/Button'
import Input from '../components/common/Input'
import { loginSchema, type LoginFormData } from '../utils/validators'
import { ROUTES } from '../types/routes'
import { useAuthStore } from '../store/authStore'
import authService from '../services/auth'

export default function Login() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login } = useAuthStore()
  const [error, setError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const fillDemoCredentials = (role: 'admin' | 'planner' | 'viewer') => {
    const credentials = {
      admin: { email: 'admin@ooumph.com', password: 'admin123' },
      planner: { email: 'admin@ooumph.com', password: 'planner123' },
      viewer: { email: 'viewer@infrastructure.ap.gov.in', password: 'viewer123' },
    }
    setValue('email', credentials[role].email)
    setValue('password', credentials[role].password)
  }

  const onSubmit = async (data: LoginFormData) => {
    setError(null)
    try {
      const tokens = await authService.login({
        email: data.email,
        password: data.password,
      })
      login(tokens)
      const redirectTo = (location.state as { redirect_to?: string })?.redirect_to || ROUTES.DASHBOARD
      navigate(redirectTo, { replace: true })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed. Please try again.')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-blue-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-6">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
            </div>
            <h1 className="text-2xl font-bold text-gray-900">
              Infrastructure Planning System
            </h1>
            <p className="text-sm text-primary-600 font-medium mt-1">
              Andhra Pradesh Roads & Buildings Department
            </p>
            <p className="text-xs text-gray-500 mt-2">
              AI-Powered Bridge & Flyover Planning
            </p>
          </div>

          <h2 className="mt-6 text-center text-lg font-semibold text-gray-800">
            Sign in to your account
          </h2>

          {error && (
            <div className="mt-4 bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <form className="mt-4 space-y-4" onSubmit={handleSubmit(onSubmit)}>
            <div className="space-y-4">
              <Input
                {...register('email')}
                type="email"
                label="Email address"
                placeholder="Enter your email"
                error={errors.email?.message}
                autoComplete="email"
              />

              <Input
                {...register('password')}
                type="password"
                label="Password"
                placeholder="Enter your password"
                error={errors.password?.message}
                autoComplete="current-password"
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                  Remember me
                </label>
              </div>

              <div className="text-sm">
                <Link
                  to={ROUTES.FORGOT_PASSWORD}
                  className="font-medium text-primary-600 hover:text-primary-500"
                >
                  Forgot password?
                </Link>
              </div>
            </div>

            <Button type="submit" className="w-full" isLoading={isSubmitting}>
              Sign in
            </Button>

            <div className="text-center">
              <span className="text-sm text-gray-600">Don't have an account? </span>
              <Link
                to={ROUTES.REGISTER}
                className="font-medium text-primary-600 hover:text-primary-500"
              >
                Sign up
              </Link>
            </div>
          </form>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-6">
          <h3 className="text-sm font-semibold text-gray-700 mb-3 text-center">
            Demo Credentials (Click to auto-fill)
          </h3>
          <div className="space-y-2">
            <button
              type="button"
              onClick={() => fillDemoCredentials('admin')}
              className="w-full flex items-center justify-between p-3 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors border border-purple-200"
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <div className="text-left">
                  <p className="text-sm font-medium text-purple-900">Administrator</p>
                  <p className="text-xs text-purple-600">Full access to all features</p>
                </div>
              </div>
              <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <button
              type="button"
              onClick={() => fillDemoCredentials('planner')}
              className="w-full flex items-center justify-between p-3 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors border border-blue-200"
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <div className="text-left">
                  <p className="text-sm font-medium text-blue-900">Infrastructure Planner</p>
                  <p className="text-xs text-blue-600">Create & analyze projects</p>
                </div>
              </div>
              <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <button
              type="button"
              onClick={() => fillDemoCredentials('viewer')}
              className="w-full flex items-center justify-between p-3 bg-green-50 hover:bg-green-100 rounded-lg transition-colors border border-green-200"
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </div>
                <div className="text-left">
                  <p className="text-sm font-medium text-green-900">Viewer</p>
                  <p className="text-xs text-green-600">Read-only access</p>
                </div>
              </div>
              <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
          <p className="mt-3 text-xs text-gray-500 text-center">
            For demo purposes only. These credentials allow full system exploration.
          </p>
        </div>

        <p className="text-center text-xs text-gray-500">
          © 2026 Ooumph AI-Enabled Bridge & Flyover Planning System
        </p>
      </div>
    </div>
  )
}
