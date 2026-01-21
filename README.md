# WikiSmart Edu - Plateforme Éducative IA

Ce projet est une plateforme éducative intelligente permettant d'ingérer des articles Wikipédia ou des PDF, de générer des résumés, des traductions, des QCM interactifs et de suivre la progression des utilisateurs.

## Structure générale

- backend/
  - app/
    - main.py (application FastAPI)
    - api/v1 (routes : auth, articles, quiz, admin, health)
    - core (config, sécurité JWT, logging, exceptions)
    - db (session SQLAlchemy, init_db)
    - models (users, articles, quizattempts)
    - schemas (Pydantic : auth, user, article, quiz, stats)
    - services (wikipedia, pdf, LLM Groq, LLM Gemini, quiz, user, stats)
  - requirements.txt
  - Dockerfile
- frontend/
  - src/
    - pages (Home, Historique, Dashboard admin, App)
    - components (formulaires d'ingestion URL/PDF, etc.)
    - services (client API Axios)
    - context (AuthContext)
  - package.json, vite.config.mts, Dockerfile
- docker-compose.yml (orchestration backend + frontend + PostgreSQL)
- .env.example (variables d'environnement)

## Démarrage rapide avec Docker

1. Copier le fichier `.env.example` vers `.env` et renseigner les clés LLM si nécessaires.
2. Depuis la racine du projet :

```bash
docker-compose up --build
```

- Backend : http://localhost:8000
- Frontend : http://localhost:5173

## Prochaines étapes de développement

- Implémenter l'authentification complète (OAuth2 + JWT) dans les routes `auth`.
- Implémenter la logique d'ingestion, de résumé, traduction et génération de QCM dans les services LLM.
- Ajouter l'export PDF/TXT côté backend et les boutons correspondants côté frontend.
- Ajouter des tests unitaires détaillés (pytest) avec mocks pour Groq et Gemini.
