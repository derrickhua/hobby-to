import handleFetch from "./fetch";
const API_BASE_URL = 'http://localhost:5000/api/hobbies';

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
