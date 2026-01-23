'use client';

import { useState, useEffect } from 'react';

// Types removed as they are now inline or replaced


export interface UserPreferences {
    userFirstName: string;
    userLastName: string;
    assistantName: string;
    assistantBehavior: 'professional' | 'friendly' | 'energetic' | 'tactical' | 'minimal';
    isOnboarded: boolean;
}

const DEFAULT_PREFERENCES: UserPreferences = {
    userFirstName: '',
    userLastName: '',
    assistantName: 'BUCKY',
    assistantBehavior: 'tactical',
    isOnboarded: false,
};

const STORAGE_KEY = 'bucky_user_preferences_v1';

export function useUserPreferences() {
    const [preferences, setPreferences] = useState<UserPreferences>(DEFAULT_PREFERENCES);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            if (stored) {
                setPreferences(JSON.parse(stored));
            }
        } catch (e) {
            console.error('Failed to load user preferences', e);
        } finally {
            setIsLoaded(true);
        }
    }, []);

    const savePreferences = (newPrefs: Partial<UserPreferences>) => {
        const updated = { ...preferences, ...newPrefs, isOnboarded: true };
        setPreferences(updated);
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
        } catch (e) {
            console.error('Failed to save user preferences', e);
        }
    };

    const resetPreferences = () => {
        setPreferences(DEFAULT_PREFERENCES);
        try {
            localStorage.removeItem(STORAGE_KEY);
        } catch (e) {
            console.error('Failed to reset user preferences', e);
        }
    };

    return {
        preferences,
        isLoaded,
        savePreferences,
        resetPreferences,
    };
}
