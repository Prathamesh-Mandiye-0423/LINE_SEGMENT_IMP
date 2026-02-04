import axios from 'axios';

const API_BASE_URL =  'https://line-segment-separator-1.onrender.com/api'|| 'http://localhost:5000/api';

export const computeRectangles = async (redSegments, blueSegments) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/compute/rectangles`, {
      red_segments: redSegments,
      blue_segments: blueSegments
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Computation failed');
    }
    throw new Error('Network error. Is the backend running?');
  }
};

export const computeSquares = async (redSegments, blueSegments, usePST = true) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/compute/squares`, {
      red_segments: redSegments,
      blue_segments: blueSegments,
      use_pst: usePST
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Computation failed');
    }
    throw new Error('Network error. Is the backend running?');
  }
};

export const generateRandomData = async (params) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/generate/random`, params);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Generation failed');
    }
    throw new Error('Network error. Is the backend running?');
  }
};

export const healthCheck = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    throw new Error('Backend is not responding');
  }
};