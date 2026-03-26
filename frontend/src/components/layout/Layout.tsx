import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import { useUIStore } from '../../store/uiStore'
import { useEffect } from 'react'

export default function Layout() {
  const { sidebarOpen, initializeTheme } = useUIStore()

  useEffect(() => {
    initializeTheme()
  }, [initializeTheme])

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 transition-colors">
      <Header />
      <Sidebar />
      <main
        className={`pt-16 min-h-screen transition-all ${
          sidebarOpen ? 'lg:ml-64' : ''
        }`}
      >
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
