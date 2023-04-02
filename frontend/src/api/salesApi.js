import { getApiCall } from "./axiosConfig";

const BASE_API_URL = "/api/v1/service-sales";

const allBookingSalesTimeApi = (adminId, filter) =>
    `${BASE_API_URL}/time?admin=${adminId}&filter=${filter}`;

const agentBookingSalesTimeApi = (agentId, filter) =>
    `${BASE_API_URL}/time/agent?agent=${agentId}&filter=${filter}`;

const userServiceSalesApi = (userId) => `${BASE_API_URL}/user?user=${userId}`;

const agentCommissionApi = (agentId) =>
    `${BASE_API_URL}/agents-commission?agent=${agentId}`;

const adminTravelServiceSalesApi = (adminId) =>
    `${BASE_API_URL}/agents?admin=${adminId}`;

export const fetchAllAgentServiceSalesAsync = async (adminId) => {
    try {
        let { data } = await getApiCall(adminTravelServiceSalesApi(adminId));
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

export const fetchUserServiceSalesAsync = async (userId) => {
    try {
        let { data } = await getApiCall(userServiceSalesApi(userId));

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

export const fetchAgentSalesCommissionAsync = async (userId) => {
    try {
        let { data } = await getApiCall(agentCommissionApi(userId));

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

export const fetchAllBookingSalesTimeAsync = async (adminId, filter) => {
    try {
        let { data } = await getApiCall(
            allBookingSalesTimeApi(adminId, filter)
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

export const fetchAgentBookingSalesTimeAsync = async (agentId, filter) => {
    try {
        let { data } = await getApiCall(
            agentBookingSalesTimeApi(agentId, filter)
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
