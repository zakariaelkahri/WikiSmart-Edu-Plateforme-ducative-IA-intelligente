import React from 'react';
import UrlIngestionForm from '../components/UrlIngestionForm.jsx';
import PdfIngestionForm from '../components/PdfIngestionForm.jsx';

function HomePage() {
    return (
        <section>
            <h2>Ingérer un article</h2>
            <UrlIngestionForm />
            <PdfIngestionForm />
        </section>
    );
}

export default HomePage;
