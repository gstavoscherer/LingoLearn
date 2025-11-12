// stores/languages.ts
import type { LanguageType } from '$lib/types';
import { writable } from 'svelte/store';

interface LanguagesStore {
    languages: LanguageType[];
    loading: boolean;
    error: string | null;
}

const initialState: LanguagesStore = {
    languages: [],
    loading: false,
    error: null
};

function createLanguagesStore() {
    const { subscribe, set, update } = writable<LanguagesStore>(initialState);

    return {
        subscribe,
        load: async () => {
            update(state => ({ ...state, loading: true, error: null }));
            
            try {
                const response = await fetch(`${import.meta.env.VITE_API_URL}/languages`);
                
                if (!response.ok) throw new Error('Failed to fetch languages');
                
                const languages: LanguageType[] = await response.json();
                
                set({ languages, loading: false, error: null });
                
                return languages;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'Unknown error';
                set({ languages: [], loading: false, error: errorMessage });
                throw error;
            }
        },
        // Opcional: método para limpar/recarregar
        clear: () => set(initialState)
    };
}

export const languagesStore = createLanguagesStore();