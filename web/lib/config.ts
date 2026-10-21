/**
 * API Configuration
 * Supports both local development and production deployment
 */

export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const API_ENDPOINTS = {
  research: `${API_URL}/api/v1/research`,
  discover: `${API_URL}/api/v1/discover`,
  analytics: `${API_URL}/api/v1/analytics`,
  history: `${API_URL}/api/v1/history`,
  settings: `${API_URL}/api/v1/settings`,
  testApi: `${API_URL}/api/v1/settings/test-api`,
};
