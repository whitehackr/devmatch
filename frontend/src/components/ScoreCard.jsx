export default function ScoreCard({ overallScore, requiredScore, preferredScore }) {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 65) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score) => {
    if (score >= 80) return 'bg-green-50 border-green-200';
    if (score >= 65) return 'bg-yellow-50 border-yellow-200';
    return 'bg-red-50 border-red-200';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 md:p-8">
      <h3 className="text-xl font-semibold text-gray-900 mb-6">Match Score</h3>

      <div className="grid md:grid-cols-3 gap-6">
        {/* Overall Score */}
        <div className={`border-2 rounded-lg p-6 text-center ${getScoreBgColor(overallScore)}`}>
          <p className="text-sm font-medium text-gray-600 mb-2">Overall Match</p>
          <p className={`text-5xl font-bold ${getScoreColor(overallScore)}`}>
            {overallScore}%
          </p>
          <p className="text-xs text-gray-500 mt-2">
            Weighted average (70% required, 30% preferred)
          </p>
        </div>

        {/* Required Score */}
        <div className={`border-2 rounded-lg p-6 text-center ${getScoreBgColor(requiredScore)}`}>
          <p className="text-sm font-medium text-gray-600 mb-2">Required Skills</p>
          <p className={`text-5xl font-bold ${getScoreColor(requiredScore)}`}>
            {requiredScore}%
          </p>
          <p className="text-xs text-gray-500 mt-2">
            Must-have skills for the role
          </p>
        </div>

        {/* Preferred Score */}
        <div className={`border-2 rounded-lg p-6 text-center ${getScoreBgColor(preferredScore)}`}>
          <p className="text-sm font-medium text-gray-600 mb-2">Preferred Skills</p>
          <p className={`text-5xl font-bold ${getScoreColor(preferredScore)}`}>
            {preferredScore}%
          </p>
          <p className="text-xs text-gray-500 mt-2">
            Nice-to-have bonus skills
          </p>
        </div>
      </div>
    </div>
  );
}
