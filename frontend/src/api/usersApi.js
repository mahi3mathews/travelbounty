import { ADMIN, AGENT } from "../constants/user_roles";
import { getApiCall, postApiCall } from "./axiosConfig";

const BASE_API_URL = "/api/v1";
const LOGIN_API_URL = `${BASE_API_URL}/login`;
const REGISTER_ADMIN_API_URL = `${BASE_API_URL}/register-admin`;
const REGISTER_AGENT_API_URL = `${BASE_API_URL}/register-agent`;
const USERS_API = `${BASE_API_URL}/users`;
const agentListAPI = (adminId) => `${BASE_API_URL}/${adminId}/agents`;
const agentDetailsAPI = (agentId) => `${BASE_API_URL}/agents/${agentId}`;

export const loginAsync = async (userDetails) => {
    try {
        const { data } = await postApiCall(LOGIN_API_URL, userDetails);

        delete data.password;
        return data?.data ?? data;
    } catch (error) {
        return {
            message:
                error?.response?.data?.error ??
                error?.response?.data?.message ??
                error.response?.data?.data,
            status: error?.response?.status,
        };
    }
};

export const registerUserAsync = async (userDetails) => {
    try {
        let isAdmin = userDetails.isAdmin;
        userDetails.role = isAdmin ? ADMIN : AGENT;
        delete userDetails.isAdmin;
        const { data } = await postApiCall(
            isAdmin ? REGISTER_ADMIN_API_URL : REGISTER_AGENT_API_URL,
            userDetails
        );
        return data?.data ?? data;
    } catch (error) {
        return {
            message:
                error?.response?.data?.error ??
                error?.response?.data?.message ??
                error.response?.data?.data,
            status: error.response?.status,
        };
    }
};

export const getUserDetailsAsync = async (userId) => {
    try {
        const { data } = await getApiCall(`${USERS_API}/${userId}`);

        return data?.data ?? data;
    } catch (error) {
        return {
            message:
                error?.response?.data?.error ??
                error?.response?.data?.message ??
                error.response?.data?.data,
            status: error.response?.status,
        };
    }
};

export const fetchAgentsAsync = async (agentId) => {
    try {
        const { data } = await getApiCall(agentListAPI(agentId));
        return data?.data;
    } catch (error) {
        return {
            message:
                error?.response?.data?.error ??
                error?.response?.data?.message ??
                error.response?.data?.data,
            status: error.response?.status,
        };
    }
};

export const fetchAgentDetailsAsync = async (agentId) => {
    try {
        const { data } = await getApiCall(agentDetailsAPI(agentId));
        return data?.data ?? data;
    } catch (error) {
        return {
            message:
                error?.response?.data?.error ??
                error?.response?.data?.message ??
                error.response?.data?.data,
            status: error.response?.status,
        };
    }
};
