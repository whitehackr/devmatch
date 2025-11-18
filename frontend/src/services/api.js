import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds (matches backend timeout)
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Analyze job match
 * @param {Object} data - Request data
 * @param {string} data.github_username - GitHub username
 * @param {string} [data.job_url] - Job URL (optional)
 * @param {string} [data.job_description] - Job description text (optional)
 * @param {Function} onProgress - Progress callback
 * @returns {Promise<Object>} Match result
 */
export const analyzeJobMatch = async (data, onProgress) => {
  try {
    if (onProgress) {
      setTimeout(() => onProgress('Analyzing job requirements...'), 0);
      setTimeout(() => onProgress('Fetching your GitHub profile...'), 10000);
      setTimeout(() => onProgress('Calculating match score...'), 30000);
    }

    const response = await apiClient.post('/api/analyze', data);
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error
      const detail = error.response.data.detail;

      if (typeof detail === 'object') {
        throw new Error(detail.message || 'Analysis failed');
      } else {
        throw new Error(detail || 'Analysis failed');
      }
    } else if (error.request) {
      // Request made but no response
      throw new Error('No response from server. Please check your connection.');
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
};

/**
 * Health check
 * @returns {Promise<Object>} Health status
 */
export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Could not connect to API');
  }
};
