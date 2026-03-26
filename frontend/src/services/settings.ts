import api from './api'
import type { Notification } from '../types/notification'

const notificationService = {
  async getNotifications(unreadOnly = false, page: number = 1, pageSize: number = 20): Promise<{ items: Notification[]; total: number }> {
    const params = new URLSearchParams()
    if (unreadOnly) params.append('unread_only', 'true')
    params.append('page', page.toString())
    params.append('page_size', pageSize.toString())
    
    const response = await api.get<{ items: Notification[]; total: number }>('/notifications', { params })
    return response.data
  },

  async markAsRead(notificationId: string): Promise<void> {
    await api.put(`/notifications/${notificationId}/read`)
  },

  async getUnreadCount(): Promise<number> {
    const response = await api.get<{unread_count: number}>('/notifications/unread-count')
    return response.data.unread_count
  },
}

export default notificationService;
