export default async function handleFetch<T>(
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