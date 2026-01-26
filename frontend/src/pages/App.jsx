import React from 'react';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import HomePage from './HomePage.jsx';
import ArticleHistoryPage from './ArticleHistoryPage.jsx';
import AdminDashboardPage from './AdminDashboardPage.jsx';
import LoginPage from './LoginPage.jsx';
import SignupPage from './SignupPage.jsx';

function App() {
    const { isAuthenticated, user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="app-container">
            <header>
                <h1>WikiSmart Edu</h1>
                <nav>
                    <Link to="/">Accueil</Link>
                    {isAuthenticated && (
                        <>
                            <Link to="/history">Historique</Link>
                            {user?.role === 'ADMIN' && <Link to="/admin">Admin</Link>}
                        </>
                    )}
                </nav>
                <div className="auth-nav">
                    {isAuthenticated ? (
                        <>
                            <span>Bonjour, {user?.username}</span>
                            <button onClick={handleLogout}>Déconnexion</button>
                        </>
                    ) : (
                        <>
                            <Link to="/login">Connexion</Link>
                            <Link to="/signup">S'inscrire</Link>
                        </>
                    )}
                </div>
            </header>

            <main>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/signup" element={<SignupPage />} />
                    <Route path="/history" element={<ArticleHistoryPage />} />
                    <Route path="/admin" element={<AdminDashboardPage />} />
                </Routes>
            </main>
        </div>
    );
}

export default App;
