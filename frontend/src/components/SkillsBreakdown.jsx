export default function SkillsBreakdown({ matchedSkills, missingSkills }) {
  const getCategoryBadgeColor = (category) => {
    const colors = {
      language: 'bg-blue-100 text-blue-800',
      framework: 'bg-purple-100 text-purple-800',
      database: 'bg-green-100 text-green-800',
      cloud: 'bg-yellow-100 text-yellow-800',
      tool: 'bg-gray-100 text-gray-800',
      concept: 'bg-pink-100 text-pink-800',
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  const getImportanceBadge = (importance) => {
    if (importance >= 5) return '🔴 Critical';
    if (importance >= 4) return '🟠 Important';
    if (importance >= 3) return '🟡 Moderate';
    return '🟢 Nice-to-have';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 md:p-8">
      <h3 className="text-xl font-semibold text-gray-900 mb-6">Skills Breakdown</h3>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Matched Skills */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-lg font-semibold text-green-700">
              ✅ Matched Skills ({matchedSkills.length})
            </h4>
          </div>

          {matchedSkills.length === 0 ? (
            <p className="text-gray-500 italic">No matched skills found</p>
          ) : (
            <div className="space-y-3">
              {matchedSkills.map((skill, index) => (
                <div
                  key={index}
                  className="border border-green-200 bg-green-50 rounded-lg p-4"
                >
                  <div className="flex items-start justify-between mb-2">
                    <span className="font-semibold text-gray-900 capitalize">
                      {skill.name}
                    </span>
                    <span
                      className={`text-xs px-2 py-1 rounded ${getCategoryBadgeColor(
                        skill.category
                      )}`}
                    >
                      {skill.category}
                    </span>
                  </div>

                  <p className="text-sm text-gray-600 mb-1">
                    {getImportanceBadge(skill.importance)}
                  </p>

                  <p className="text-sm text-green-700 font-medium">
                    {skill.evidence}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Missing Skills */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-lg font-semibold text-red-700">
              ❌ Missing Skills ({missingSkills.length})
            </h4>
          </div>

          {missingSkills.length === 0 ? (
            <p className="text-green-600 font-medium">
              🎉 No missing skills! Perfect match!
            </p>
          ) : (
            <div className="space-y-3">
              {missingSkills.map((skill, index) => (
                <div
                  key={index}
                  className="border border-red-200 bg-red-50 rounded-lg p-4"
                >
                  <div className="flex items-start justify-between mb-2">
                    <span className="font-semibold text-gray-900 capitalize">
                      {skill.name}
                    </span>
                    <span
                      className={`text-xs px-2 py-1 rounded ${getCategoryBadgeColor(
                        skill.category
                      )}`}
                    >
                      {skill.category}
                    </span>
                  </div>

                  <p className="text-sm text-gray-600">
                    {getImportanceBadge(skill.importance)}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
