import ScoreCard from './ScoreCard';
import RecommendationCard from './RecommendationCard';
import SkillsBreakdown from './SkillsBreakdown';
import GitHubProfileSummary from './GitHubProfileSummary';
import JobDetailsSummary from './JobDetailsSummary';

export default function Results({ result, onReset }) {
  return (
    <div className="space-y-6">
      {/* Header with Reset Button */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Analysis Results</h2>
        <button
          onClick={onReset}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          New Analysis
        </button>
      </div>

      {/* Score Card */}
      <ScoreCard
        overallScore={result.overall_score}
        requiredScore={result.required_score}
        preferredScore={result.preferred_score}
      />

      {/* Recommendation Card */}
      <RecommendationCard
        recommendation={result.recommendation}
        recommendationText={result.recommendation_text}
        gapAnalysis={result.gap_analysis}
      />

      {/* Skills Breakdown */}
      <SkillsBreakdown
        matchedSkills={result.matched_skills}
        missingSkills={result.missing_skills}
      />

      {/* GitHub Profile Summary */}
      <GitHubProfileSummary profile={result.github_profile} />

      {/* Job Details Summary */}
      <JobDetailsSummary jobDescription={result.job_description} />
    </div>
  );
}
