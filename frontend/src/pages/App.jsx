import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import HomePage from './HomePage.jsx';
import ArticleHistoryPage from './ArticleHistoryPage.jsx';
import AdminDashboardPage from './AdminDashboardPage.jsx';

function App() {
    return (
        <div className="app-container">
            <header>
                <h1>WikiSmart Edu</h1>
                <nav>
                    <Link to="/">Accueil</Link>
                    <Link to="/history">Historique</Link>
                    <Link to="/admin">Admin</Link>
                </nav>
            </header>

            <main>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/history" element={<ArticleHistoryPage />} />
                    <Route path="/admin" element={<AdminDashboardPage />} />
                </Routes>
            </main>
        </div>
    );
}

export default App;
