// src/util/hobbies.ts
const API_BASE_URL = 'http://localhost:5000/api/hobbies';

async function handleFetch<T>(url: string, errorMessagePrefix: string): Promise<T> {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`${errorMessagePrefix} - HTTP status: ${response.status}`);
        }
        return await response.json() as T;
    } catch (error) {
        console.error(`${errorMessagePrefix} - ${error}`);
        throw error;
    }
}

export function searchHobbies({ query = '', cost = [], category = null }){
    const costQuery = cost.join('&cost=');
    const url = `${API_BASE_URL}/search?query=${query}&cost=${costQuery}&category=${category || ''}`;
    return handleFetch(url, "Error searching hobbies");
}

export function getHobbiesByCategory(category: string) {
    const url = `${API_BASE_URL}/category?category=${category}`;
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
