import { writable } from 'svelte/store';

async function checkAuthStatus() {
    try {
        const response = await fetch('/api/users/me');  // Endpoint that checks user's auth status
        return response.ok;
    } catch (error) {
        console.error('Error checking auth status', error);
        return false;
    }
}

function createAuthStore() {
    const { subscribe, set } = writable(false);  // Start with false indicating not logged in

    checkAuthStatus().then(isLoggedIn => set(isLoggedIn));

    return {
        subscribe
        // No login or logout actions here as they are handled via HTTP-only cookies
    };
}

export const auth = createAuthStore();