import React from 'react';
import { useAuth } from '../context/AuthContext.jsx';
import SummaryForm from '../components/UrlIngestionForm.jsx';
import TranslationForm from '../components/PdfIngestionForm.jsx';
import QuizForm from '../components/QuizForm.jsx';

function HomePage() {
    const { isAuthenticated } = useAuth();

    if (!isAuthenticated) {
        return (
            <section className="welcome-section">
                <h2>Bienvenue sur WikiSmart Edu</h2>
                <p>Veuillez vous connecter pour accéder aux fonctionnalités IA.</p>
            </section>
        );
    }

    return (
        <section className="features-section">
            <h2>Fonctionnalités IA Wikipedia</h2>
            <div className="features-grid">
                <SummaryForm />
                <TranslationForm />
                <QuizForm />
            </div>
        </section>
    );
}

export default HomePage;
