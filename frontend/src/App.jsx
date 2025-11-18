import { useState } from 'react';
import InputForm from './components/InputForm';
import LoadingState from './components/LoadingState';
import Results from './components/Results';
import Header from './components/Header';
import { analyzeJobMatch } from './services/api';

function App() {
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setLoadingMessage('Starting analysis...');

    try {
      const data = await analyzeJobMatch(formData, (message) => {
        setLoadingMessage(message);
      });

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      setLoadingMessage('');
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {!loading && !result && (
          <InputForm onSubmit={handleAnalyze} error={error} />
        )}

        {loading && <LoadingState message={loadingMessage} />}

        {result && <Results result={result} onReset={handleReset} />}
      </main>

      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-6 text-center text-gray-600 text-sm">
          <p>
            DevMatch analyzes your GitHub repositories to match against job requirements.
          </p>
          <p className="mt-2">
            Built with FastAPI, React, and deployed on Railway + Vercel.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
