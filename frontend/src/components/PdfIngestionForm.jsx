import React, { useState } from 'react';
import { translateArticleByUrl } from '../services/apiClient.js';

function TranslationForm() {
    const [url, setUrl] = useState('');
    const [targetLanguage, setTargetLanguage] = useState('FR');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [result, setResult] = useState(null);

    const languages = [
        { code: 'FR', name: 'Français' },
        { code: 'EN', name: 'English' },
        { code: 'AR', name: 'العربية' },
        { code: 'ES', name: 'Español' },
        { code: 'DE', name: 'Deutsch' },
        { code: 'IT', name: 'Italiano' },
    ];

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setResult(null);
        setLoading(true);

        try {
            const data = await translateArticleByUrl(url, targetLanguage);
            setResult(data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to translate article. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="feature-card">
            <h3>🌐 Traduire un Article</h3>
            <form onSubmit={handleSubmit} className="feature-form">
                <div className="form-group">
                    <label htmlFor="translate-url">URL Wikipedia</label>
                    <input
                        type="url"
                        id="translate-url"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        placeholder="https://en.wikipedia.org/wiki/..."
                        required
                        disabled={loading}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="target-language">Langue cible</label>
                    <select
                        id="target-language"
                        value={targetLanguage}
                        onChange={(e) => setTargetLanguage(e.target.value)}
                        disabled={loading}
                    >
                        {languages.map((lang) => (
                            <option key={lang.code} value={lang.code}>
                                {lang.name}
                            </option>
                        ))}
                    </select>
                </div>

                <button type="submit" disabled={loading} className="submit-button">
                    {loading ? 'Traduction...' : 'Traduire'}
                </button>
            </form>

            {error && <div className="error-message">{error}</div>}

            {result && (
                <div className="result-box">
                    <h4>{result.title}</h4>
                    <div className="result-content">
                        <p className="translated-text">{result.translated_text}</p>
                    </div>
                </div>
            )}
        </div>
    );
}

export default TranslationForm;
