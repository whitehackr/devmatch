export default function LoadingState({ message }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-12 text-center">
      <div className="flex flex-col items-center justify-center space-y-6">
        {/* Spinner */}
        <div className="relative">
          <div className="w-24 h-24 border-8 border-gray-200 border-t-blue-600 rounded-full animate-spin"></div>
        </div>

        {/* Message */}
        <div className="space-y-2">
          <h2 className="text-2xl font-bold text-gray-900">
            Analyzing Your Match
          </h2>
          <p className="text-gray-600 max-w-md">
            {message || 'This may take 30-60 seconds...'}
          </p>
        </div>

        {/* Progress Steps */}
        <div className="max-w-md w-full space-y-3 text-left">
          <div className="flex items-start space-x-3 text-sm">
            <svg
              className="w-5 h-5 text-blue-600 mt-0.5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            <span className="text-gray-700">Extracting skills from job description</span>
          </div>

          <div className="flex items-start space-x-3 text-sm">
            <svg
              className="w-5 h-5 text-gray-400 mt-0.5 animate-pulse"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            <span className="text-gray-700">Analyzing your GitHub repositories</span>
          </div>

          <div className="flex items-start space-x-3 text-sm">
            <svg
              className="w-5 h-5 text-gray-300 mt-0.5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            <span className="text-gray-700">Calculating match score</span>
          </div>
        </div>
      </div>
    </div>
  );
}
