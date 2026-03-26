import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuthStore } from '../store/authStore'
import authService from '../services/auth'
import Button from '../components/common/Button'
import Input from '../components/common/Input'

const profileSchema = z.object({
  fullName: z.string().min(1, 'Name is required').min(2, 'Name must be at least 2 characters'),
})

const passwordSchema = z.object({
  currentPassword: z.string().min(1, 'Current password is required'),
  newPassword: z
    .string()
    .min(1, 'New password is required')
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),
  confirmPassword: z.string().min(1, 'Please confirm your password'),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
})

type ProfileFormData = z.infer<typeof profileSchema>
type PasswordFormData = z.infer<typeof passwordSchema>

export default function Profile() {
  const { user, setUser } = useAuthStore()
  const [profileError, setProfileError] = useState<string | null>(null)
  const [profileSuccess, setProfileSuccess] = useState<string | null>(null)
  const [passwordError, setPasswordError] = useState<string | null>(null)
  const [passwordSuccess, setPasswordSuccess] = useState<string | null>(null)
  const [loadingUser, setLoadingUser] = useState(!user)

  const {
    register: registerProfile,
    handleSubmit: handleProfileSubmit,
    formState: { errors: profileErrors, isSubmitting: isProfileSubmitting },
    reset: resetProfile,
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      fullName: user?.fullName || '',
    },
  })

  const {
    register: registerPassword,
    handleSubmit: handlePasswordSubmit,
    formState: { errors: passwordErrors, isSubmitting: isPasswordSubmitting },
    reset: resetPassword,
  } = useForm<PasswordFormData>({
    resolver: zodResolver(passwordSchema),
  })

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const userData = await authService.getProfile()
        setUser(userData)
        resetProfile({ fullName: userData.fullName })
      } catch (err) {
        console.error('Failed to fetch profile:', err)
      } finally {
        setLoadingUser(false)
      }
    }

    if (!user) {
      fetchProfile()
    }
  }, [user, setUser, resetProfile])

  useEffect(() => {
    if (user) {
      resetProfile({ fullName: user.fullName })
    }
  }, [user, resetProfile])

  const onProfileSubmit = async (data: ProfileFormData) => {
    setProfileError(null)
    setProfileSuccess(null)
    try {
      const updatedUser = await authService.updateProfile({ fullName: data.fullName })
      setUser(updatedUser)
      setProfileSuccess('Profile updated successfully!')
    } catch (err) {
      setProfileError(err instanceof Error ? err.message : 'Failed to update profile')
    }
  }

  const onPasswordSubmit = async (data: PasswordFormData) => {
    setPasswordError(null)
    setPasswordSuccess(null)
    try {
      await authService.updateProfile({ 
        currentPassword: data.currentPassword,
        newPassword: data.newPassword 
      } as Partial<typeof user> & { currentPassword: string; newPassword: string })
      setPasswordSuccess('Password changed successfully!')
      resetPassword()
    } catch (err) {
      setPasswordError(err instanceof Error ? err.message : 'Failed to change password')
    }
  }

  if (loadingUser) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case 'admin':
        return 'bg-danger-100 text-danger-700'
      case 'planner':
        return 'bg-primary-100 text-primary-700'
      case 'viewer':
        return 'bg-gray-100 text-gray-700'
      default:
        return 'bg-gray-100 text-gray-700'
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Profile</h1>
        <p className="text-gray-600 mt-1">Manage your account settings</p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Account Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-500">Email</label>
            <p className="mt-1 text-gray-900">{user?.email}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-500">Role</label>
            <div className="mt-1">
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${getRoleBadgeColor(user?.role || '')}`}>
                {user?.role}
              </span>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-500">Status</label>
            <div className="mt-1">
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${user?.isActive ? 'bg-success-100 text-success-700' : 'bg-gray-100 text-gray-700'}`}>
                {user?.isActive ? 'Active' : 'Inactive'}
              </span>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-500">Member Since</label>
            <p className="mt-1 text-gray-900">{user?.createdAt ? formatDate(user.createdAt) : 'N/A'}</p>
          </div>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Edit Profile</h2>
        
        {profileError && (
          <div className="mb-4 bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded-lg">
            {profileError}
          </div>
        )}
        
        {profileSuccess && (
          <div className="mb-4 bg-success-50 border border-success-200 text-success-700 px-4 py-3 rounded-lg">
            {profileSuccess}
          </div>
        )}

        <form onSubmit={handleProfileSubmit(onProfileSubmit)} className="space-y-4">
          <Input
            {...registerProfile('fullName')}
            type="text"
            label="Full Name"
            placeholder="Enter your full name"
            error={profileErrors.fullName?.message}
          />

          <div className="flex justify-end">
            <Button type="submit" isLoading={isProfileSubmitting}>
              Save Changes
            </Button>
          </div>
        </form>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Change Password</h2>
        
        {passwordError && (
          <div className="mb-4 bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded-lg">
            {passwordError}
          </div>
        )}
        
        {passwordSuccess && (
          <div className="mb-4 bg-success-50 border border-success-200 text-success-700 px-4 py-3 rounded-lg">
            {passwordSuccess}
          </div>
        )}

        <form onSubmit={handlePasswordSubmit(onPasswordSubmit)} className="space-y-4">
          <Input
            {...registerPassword('currentPassword')}
            type="password"
            label="Current Password"
            placeholder="Enter your current password"
            error={passwordErrors.currentPassword?.message}
            autoComplete="current-password"
          />

          <Input
            {...registerPassword('newPassword')}
            type="password"
            label="New Password"
            placeholder="Enter your new password"
            error={passwordErrors.newPassword?.message}
            autoComplete="new-password"
          />

          <Input
            {...registerPassword('confirmPassword')}
            type="password"
            label="Confirm New Password"
            placeholder="Confirm your new password"
            error={passwordErrors.confirmPassword?.message}
            autoComplete="new-password"
          />

          <div className="flex justify-end">
            <Button type="submit" isLoading={isPasswordSubmitting}>
              Change Password
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}
