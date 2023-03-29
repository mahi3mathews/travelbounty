import axios from "axios";

// Setting up the configuration for all API calls.

// BASE_API_URL is set up in .env file
const apiCall = axios.create({
    baseURL: process.env.REACT_APP_BASE_API_URL,
    headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
    },
});

const postApiCall = (url, requestBody) => {
    return apiCall.post(url, requestBody).then((res) => res);
};
const getApiCall = (url) => apiCall.get(url).then((res) => res);
const putApiCall = (url, requestBody) =>
    apiCall.put(url, requestBody).then((res) => res);
const deleteApiCall = (url) => apiCall.delete(url).then((res) => res);

export { postApiCall, putApiCall, getApiCall, deleteApiCall };
