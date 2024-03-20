// src/util/hobbies.ts
const API_BASE_URL = 'http://localhost:5000/api/hobbies';

async function handleFetch<T>(
    url: string,
    errorMessagePrefix: string,
    options?: RequestInit
): Promise<T> {
    const defaultOptions: RequestInit = {
        method: 'GET',
    };

    // Use defaultOptions as the base, and override with provided options if any
    const fetchOptions = options ? { ...defaultOptions, ...options } : defaultOptions;

    try {
        const response = await fetch(url, fetchOptions);
        if (!response.ok) {
            throw new Error(`${errorMessagePrefix} - HTTP status: ${response.status}`);
        }
        return await response.json() as T;
    } catch (error) {
        console.error(`${errorMessagePrefix} - ${error}`);
        throw error;
    }
}

export async function searchHobbies({ query = '', cost = [], category = null }) {
    const url = `${API_BASE_URL}/search`;
    const body = { query, cost, category };
    const options: RequestInit = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    };

    return handleFetch(url, "Error searching hobbies", options);
}

export function getHobbiesByCategory(category: string) {
    const url = `${API_BASE_URL}/category?category=${encodeURIComponent(category)}`;
    return handleFetch(url, "Error fetching hobbies by category");
}

export function getHobby(hobbyId: number) {
    const url = `${API_BASE_URL}/${hobbyId}`;
    return handleFetch(url, `Error fetching details for hobby ID ${hobbyId}`);
}

export function getHobbyLocations(hobbyId: number) {
    const url = `${API_BASE_URL}/${hobbyId}/locations`;
    return handleFetch(url, `Error fetching locations for hobby ID ${hobbyId}`);
}
