import React, { useState } from 'react';
import { ingestArticleFromPdf } from '../services/apiClient.js';

function PdfIngestionForm() {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;
        setLoading(true);
        setError(null);
        try {
            await ingestArticleFromPdf(file);
            // TODO: afficher contenu et fonctionnalités IA
        } catch (err) {
            setError('Erreur lors de l\'ingestion du PDF');
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Fichier PDF:
                <input
                    type="file"
                    accept="application/pdf"
                    onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                />
            </label>
            <button type="submit" disabled={loading || !file}>
                {loading ? 'Chargement...' : 'Ingestion depuis PDF'}
            </button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </form>
    );
}

export default PdfIngestionForm;
