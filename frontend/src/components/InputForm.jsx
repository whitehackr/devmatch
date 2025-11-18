import { useState } from 'react';

export default function InputForm({ onSubmit, error }) {
  const [githubUsername, setGithubUsername] = useState('');
  const [inputMode, setInputMode] = useState('paste'); // 'paste' or 'url'
  const [jobDescription, setJobDescription] = useState('');
  const [jobUrl, setJobUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const data = {
      github_username: githubUsername.trim(),
    };

    if (inputMode === 'paste') {
      data.job_description = jobDescription.trim();
    } else {
      data.job_url = jobUrl.trim();
    }

    onSubmit(data);
  };

  const isValid =
    githubUsername.trim() &&
    ((inputMode === 'paste' && jobDescription.trim().length >= 50) ||
      (inputMode === 'url' && jobUrl.trim()));

  return (
    <div className="bg-white rounded-lg shadow-md p-6 md:p-8">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Analyze Your Match
        </h2>
        <p className="text-gray-600">
          See how well your GitHub profile matches a job description
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* GitHub Username */}
        <div>
          <label
            htmlFor="github-username"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            GitHub Username <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="github-username"
            value={githubUsername}
            onChange={(e) => setGithubUsername(e.target.value)}
            placeholder="octocat"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
          <p className="mt-1 text-sm text-gray-500">
            Your public GitHub profile will be analyzed
          </p>
        </div>

        {/* Input Mode Toggle */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Job Description Source <span className="text-red-500">*</span>
          </label>
          <div className="flex space-x-4 mb-4">
            <button
              type="button"
              onClick={() => setInputMode('paste')}
              className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                inputMode === 'paste'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Paste Text (Recommended)
            </button>
            <button
              type="button"
              onClick={() => setInputMode('url')}
              className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                inputMode === 'url'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Job URL
            </button>
          </div>
        </div>

        {/* Job Description (Paste) */}
        {inputMode === 'paste' && (
          <div>
            <label
              htmlFor="job-description"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Job Description <span className="text-red-500">*</span>
            </label>
            <textarea
              id="job-description"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the full job description here...&#10;&#10;Example:&#10;We are seeking a Senior Python Engineer with 5+ years experience.&#10;&#10;Required Skills:&#10;- Python, Django&#10;- PostgreSQL&#10;- AWS&#10;..."
              rows={12}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
              required
            />
            <p className="mt-1 text-sm text-gray-500">
              Minimum 50 characters. Include required and preferred skills for best results.
            </p>
          </div>
        )}

        {/* Job URL */}
        {inputMode === 'url' && (
          <div>
            <label
              htmlFor="job-url"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Job Posting URL <span className="text-red-500">*</span>
            </label>
            <input
              type="url"
              id="job-url"
              value={jobUrl}
              onChange={(e) => setJobUrl(e.target.value)}
              placeholder="https://www.indeed.com/viewjob?jk=..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <p className="mt-1 text-sm text-gray-500">
              Supported: Indeed, Google Jobs, LinkedIn (Note: scraping may fail, paste is more reliable)
            </p>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex">
              <svg
                className="w-5 h-5 text-red-400 mr-2"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!isValid}
          className={`w-full py-4 px-6 rounded-lg font-semibold text-white text-lg transition-all ${
            isValid
              ? 'bg-blue-600 hover:bg-blue-700 shadow-lg hover:shadow-xl'
              : 'bg-gray-300 cursor-not-allowed'
          }`}
        >
          Analyze Match
        </button>
      </form>
    </div>
  );
}
