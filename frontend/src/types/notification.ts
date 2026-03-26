export interface User {
    id: string;
    email: string;
    fullName: string;
    role: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface NotificationPreferences {
    email_notifications: boolean;
    push_notifications: boolean;
    alert_notifications: boolean;
}

export interface DisplayPreferences {
    theme: string;
    language: string;
    timezone: string;
}

export interface DashboardPreferences {
    default_view: string;
    items_per_page: number;
}

export interface UserSettings {
    notification_preferences: NotificationPreferences;
    display_preferences: DisplayPreferences;
    dashboard_preferences: DashboardPreferences;
}

export interface Settings {
    user_id: string;
    settings: UserSettings;
}

export interface SettingsUpdate {
    notification_preferences?: NotificationPreferences;
    display_preferences?: DisplayPreferences;
    dashboard_preferences?: DashboardPreferences;
}

export interface SettingsResponse {
    settings: UserSettings;
    user_id: string;
}

export interface Notification {
    id: string;
    user_id: string;
    title: string;
    message: string;
    type: string;
    is_read: boolean;
    created_at: string;
}
