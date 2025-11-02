// Task store for managing application state
import { writable } from 'svelte/store';

export const tasks = writable([]);
export const loading = writable(false);
export const error = writable(null);
export const theme = writable('light');