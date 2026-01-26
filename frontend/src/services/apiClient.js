import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
});

// Set auth token for all requests
export function setAuthToken(token) {
    if (token) {
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
        delete api.defaults.headers.common['Authorization'];
    }
}

// Auth endpoints
export async function login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await api.post('/auth/login', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });
    return response.data;
}

export async function register(userData) {
    const response = await api.post('/auth/register', userData);
    return response.data;
}

export async function ingestArticleFromUrl(url) {
    const response = await api.post('/articles/ingest/url', { url });
    return response.data;
}

export async function ingestArticleFromPdf(file) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/articles/ingest/pdf', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
}

// Article Summary endpoints
export async function summarizeArticleByUrl(url, length = 'medium') {
    const response = await api.post('/articles/summary/url', { url, length });
    return response.data;
}

// Article Translation endpoints
export async function translateArticleByUrl(url, target_language) {
    const response = await api.post('/articles/translate/url', {
        url,
        target_language
    });
    return response.data;
}

// Quiz endpoints
export async function generateQuiz(url) {
    const response = await api.post('/quiz/generate', { url });
    return response.data;
}

export async function submitQuizAttempt(article_id, answers_mcq, answers_open) {
    const response = await api.post('/quiz/attempt', {
        article_id,
        answers_mcq,
        answers_open,
    });
    return response.data;
}

// Admin endpoints
export async function getGlobalStats() {
    const response = await api.get('/admin/stats');
    return response.data;
}

// Health check
export async function healthCheck() {
    const response = await api.get('/health');
    return response.data;
}
