export default function JobDetailsSummary({ jobDescription }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 md:p-8">
      <h3 className="text-xl font-semibold text-gray-900 mb-6">
        Job Description Summary
      </h3>

      <div className="space-y-4">
        {/* Job Info */}
        {(jobDescription.title || jobDescription.company) && (
          <div className="pb-4 border-b border-gray-200">
            {jobDescription.title && (
              <p className="text-lg font-semibold text-gray-900">
                {jobDescription.title}
              </p>
            )}
            {jobDescription.company && (
              <p className="text-gray-600">{jobDescription.company}</p>
            )}
            <p className="text-sm text-gray-500 mt-1">
              Source: {jobDescription.source}
            </p>
          </div>
        )}

        {/* Skills Summary */}
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-gray-900 mb-3">
              Required Skills ({jobDescription.required_skills.length})
            </h4>
            <div className="space-y-2">
              {jobDescription.required_skills.map((skill, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between text-sm"
                >
                  <span className="text-gray-700 capitalize">{skill.name}</span>
                  <span className="text-gray-500">
                    {'⭐'.repeat(skill.importance)}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-gray-900 mb-3">
              Preferred Skills ({jobDescription.preferred_skills.length})
            </h4>
            <div className="space-y-2">
              {jobDescription.preferred_skills.map((skill, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between text-sm"
                >
                  <span className="text-gray-700 capitalize">{skill.name}</span>
                  <span className="text-gray-500">
                    {'⭐'.repeat(skill.importance)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
