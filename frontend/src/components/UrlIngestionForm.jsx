import React, { useState } from 'react';
import { summarizeArticleByUrl } from '../services/apiClient.js';

function SummaryForm() {
    const [url, setUrl] = useState('');
    const [length, setLength] = useState('medium');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [result, setResult] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setResult(null);
        setLoading(true);

        try {
            const data = await summarizeArticleByUrl(url, length);
            setResult(data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to generate summary. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="feature-card">
            <h3>📝 Générer un Résumé</h3>
            <form onSubmit={handleSubmit} className="feature-form">
                <div className="form-group">
                    <label htmlFor="summary-url">URL Wikipedia</label>
                    <input
                        type="url"
                        id="summary-url"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        placeholder="https://fr.wikipedia.org/wiki/..."
                        required
                        disabled={loading}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="length">Longueur</label>
                    <select
                        id="length"
                        value={length}
                        onChange={(e) => setLength(e.target.value)}
                        disabled={loading}
                    >
                        <option value="short">Court</option>
                        <option value="medium">Moyen</option>
                    </select>
                </div>

                <button type="submit" disabled={loading} className="submit-button">
                    {loading ? 'Génération...' : 'Générer le Résumé'}
                </button>
            </form>

            {error && <div className="error-message">{error}</div>}

            {result && (
                <div className="result-box">
                    <h4>{result.title}</h4>
                    <div className="result-content">
                        <p>{result.summary}</p>
                    </div>
                </div>
            )}
        </div>
    );
}

export default SummaryForm;
