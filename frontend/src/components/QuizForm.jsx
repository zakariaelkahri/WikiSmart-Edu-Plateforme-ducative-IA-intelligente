import React, { useState } from 'react';
import { generateQuiz } from '../services/apiClient.js';

function QuizForm() {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [quiz, setQuiz] = useState(null);
    const [userAnswersMCQ, setUserAnswersMCQ] = useState({});
    const [userAnswersOpen, setUserAnswersOpen] = useState({});
    const [showResults, setShowResults] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setQuiz(null);
        setUserAnswersMCQ({});
        setUserAnswersOpen({});
        setShowResults(false);
        setLoading(true);

        try {
            const data = await generateQuiz(url);
            setQuiz(data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to generate quiz. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleMCQAnswer = (questionIndex, optionIndex) => {
        setUserAnswersMCQ((prev) => ({
            ...prev,
            [questionIndex]: optionIndex,
        }));
    };

    const handleOpenAnswer = (questionIndex, answer) => {
        setUserAnswersOpen((prev) => ({
            ...prev,
            [questionIndex]: answer,
        }));
    };

    const handleCheckAnswers = () => {
        setShowResults(true);
    };

    const calculateScore = () => {
        let correct = 0;
        let total = 0;

        quiz.multiple_choice?.forEach((q, idx) => {
            total++;
            if (userAnswersMCQ[idx] === q.correct_index) {
                correct++;
            }
        });

        return { correct, total };
    };

    return (
        <div className="feature-card">
            <h3> Générer un Quiz</h3>
            <form onSubmit={handleSubmit} className="feature-form">
                <div className="form-group">
                    <label htmlFor="quiz-url">URL Wikipedia</label>
                    <input
                        type="url"
                        id="quiz-url"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        placeholder="https://fr.wikipedia.org/wiki/..."
                        required
                        disabled={loading}
                    />
                </div>

                <button type="submit" disabled={loading} className="submit-button">
                    {loading ? 'Générer...' : 'Générer le Quiz'}
                </button>
            </form>

            {error && <div className="error-message">{error}</div>}

            {quiz && (
                <div className="quiz-container">
                    <h4>Questions à Choix Multiples</h4>
                    {quiz.multiple_choice?.map((q, qIdx) => (
                        <div key={qIdx} className="quiz-question">
                            <p className="question-text">
                                <strong>Q{qIdx + 1}:</strong> {q.question}
                            </p>
                            <div className="options">
                                {q.options?.map((option, oIdx) => (
                                    <label
                                        key={oIdx}
                                        className={`option ${
                                            showResults && q.correct_index === oIdx
                                                ? 'correct'
                                                : showResults && userAnswersMCQ[qIdx] === oIdx
                                                ? 'incorrect'
                                                : ''
                                        }`}
                                    >
                                        <input
                                            type="radio"
                                            name={`mcq-${qIdx}`}
                                            checked={userAnswersMCQ[qIdx] === oIdx}
                                            onChange={() => handleMCQAnswer(qIdx, oIdx)}
                                            disabled={showResults}
                                        />
                                        {option}
                                    </label>
                                ))}
                            </div>
                        </div>
                    ))}

                    {quiz.open_questions && quiz.open_questions.length > 0 && (
                        <>
                            <h4>Questions Ouvertes</h4>
                            {quiz.open_questions.map((q, qIdx) => (
                                <div key={qIdx} className="quiz-question">
                                    <p className="question-text">
                                        <strong>Q{qIdx + 1}:</strong> {q.question}
                                    </p>
                                    <textarea
                                        value={userAnswersOpen[qIdx] || ''}
                                        onChange={(e) => handleOpenAnswer(qIdx, e.target.value)}
                                        placeholder="Votre r�ponse..."
                                        disabled={showResults}
                                        rows={3}
                                    />
                                    {showResults && (
                                        <div className="correct-answer">
                                            <strong>Réponse correcte:</strong> {q.answer}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </>
                    )}

                    {!showResults ? (
                        <button onClick={handleCheckAnswers} className="submit-button">
                            Vérifier les Réponses
                        </button>
                    ) : (
                        <div className="quiz-score">
                            <h4>Résultats</h4>
                            <p>
                                Score QCM: {calculateScore().correct} / {calculateScore().total}
                            </p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default QuizForm;
