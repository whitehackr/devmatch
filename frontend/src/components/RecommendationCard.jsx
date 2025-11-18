export default function RecommendationCard({ recommendation, recommendationText, gapAnalysis }) {
  const getRecommendationStyle = () => {
    switch (recommendation) {
      case 'APPLY_NOW':
        return {
          bg: 'bg-green-50',
          border: 'border-green-200',
          icon: 'text-green-600',
          title: 'text-green-900',
          emoji: '🚀',
        };
      case 'COMPETITIVE':
        return {
          bg: 'bg-yellow-50',
          border: 'border-yellow-200',
          icon: 'text-yellow-600',
          title: 'text-yellow-900',
          emoji: '💪',
        };
      case 'SKILL_GAP':
        return {
          bg: 'bg-red-50',
          border: 'border-red-200',
          icon: 'text-red-600',
          title: 'text-red-900',
          emoji: '📚',
        };
      default:
        return {
          bg: 'bg-gray-50',
          border: 'border-gray-200',
          icon: 'text-gray-600',
          title: 'text-gray-900',
          emoji: '🤔',
        };
    }
  };

  const style = getRecommendationStyle();

  return (
    <div className={`${style.bg} border-2 ${style.border} rounded-lg p-6 md:p-8`}>
      <div className="flex items-start space-x-4">
        <div className="text-5xl">{style.emoji}</div>

        <div className="flex-1">
          <h3 className={`text-2xl font-bold ${style.title} mb-2`}>
            {recommendation === 'APPLY_NOW' && 'Strong Match - Apply Now!'}
            {recommendation === 'COMPETITIVE' && 'Competitive Candidate'}
            {recommendation === 'SKILL_GAP' && 'Skill Gap Identified'}
          </h3>

          <p className="text-gray-700 text-lg mb-4">{recommendationText}</p>

          {/* Gap Analysis */}
          {gapAnalysis && (
            <div className="grid grid-cols-3 gap-4 mt-6 pt-6 border-t border-gray-200">
              <div>
                <p className="text-sm text-gray-600">Critical Missing</p>
                <p className={`text-2xl font-bold ${style.icon}`}>
                  {gapAnalysis.critical_missing}
                </p>
              </div>

              <div>
                <p className="text-sm text-gray-600">Total Gaps</p>
                <p className={`text-2xl font-bold ${style.icon}`}>
                  {gapAnalysis.total_missing}
                </p>
              </div>

              <div>
                <p className="text-sm text-gray-600">Learning Time</p>
                <p className={`text-2xl font-bold ${style.icon}`}>
                  {gapAnalysis.learning_estimate_weeks}w
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
