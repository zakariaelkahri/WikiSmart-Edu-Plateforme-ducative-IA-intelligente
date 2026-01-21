import React, { useState } from 'react';
import { ingestArticleFromUrl } from '../services/apiClient.js';

function UrlIngestionForm() {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            await ingestArticleFromUrl(url);
            // TODO: afficher le résumé, traduction, QCM, etc.
        } catch (err) {
            setError('Erreur lors de l\'ingestion de l\'article');
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                URL Wikipedia:
                <input
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://fr.wikipedia.org/wiki/..."
                    required
                />
            </label>
            <button type="submit" disabled={loading}>
                {loading ? 'Chargement...' : 'Ingestion depuis URL'}
            </button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </form>
    );
}

export default UrlIngestionForm;
