import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
});

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

// TODO: ajouter les appels pour résumé, traduction, génération de QCM, historique, stats admin, etc.
