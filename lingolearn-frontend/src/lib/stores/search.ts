import { writable } from 'svelte/store';

export const searchStore = writable<string>();

export const searchActions = {
    clear: () => searchStore.set(''),
    update: (value: string) => searchStore.set(value)
};