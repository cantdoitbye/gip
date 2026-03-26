
export interface NotificationPreferences {
    email_notifications: boolean
    push_notifications: boolean
    alert_notifications: boolean
}

 export interface DisplayPreferences {
    theme: 'light' | 'dark'
    language: 'en' | 'hi'
    timezone: string
}
export interface DashboardPreferences {
    default_view: 'grid' | 'list'
    items_per_page: number
}
export interface UserSettings {
    notification_preferences: NotificationPreferences
    display_preferences: DisplayPreferences
    dashboard_preferences: DashboardPreferences
}
