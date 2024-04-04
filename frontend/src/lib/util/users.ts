import handleFetch from "./fetch";
const API_BASE_URL = 'http://localhost:5000/api/users';

export async function register(email: string, username: string, password: string) {
    const url = `${API_BASE_URL}/register`;
    const body = { email, username, password };
    const options: RequestInit = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    };

    return handleFetch(url, "Error registering user", options);
}

export async function login(email: string, password: string) {
    const url = `${API_BASE_URL}/login`;
    const body = { email, password };
    const options: RequestInit = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    };

    return handleFetch(url, "Error logging in user", options);
}
