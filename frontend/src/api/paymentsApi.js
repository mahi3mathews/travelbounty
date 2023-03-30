import { getApiCall, postApiCall, putApiCall } from "./axiosConfig";

const basePaymentAPI = (userId) => `/api/v1/${userId}/payments`;

const incentiveAPI = (userId, agentId) =>
    `${basePaymentAPI(userId)}/${agentId}/incentive`;

const allPaymentsAPI = (userId, status) =>
    `${basePaymentAPI(userId)}?status=${status}`;

const userPaymentsAPI = (userId, status) =>
    `${basePaymentAPI(userId)}/user?status=${status}`;

const singlePaymentAPI = (userId, agentId) =>
    `${basePaymentAPI(userId)}/pay/${agentId}`;

export const addAgentIncentiveAsync = async (payload, agentId, userId) => {
    try {
        let { data } = await postApiCall(
            incentiveAPI(userId, agentId),
            payload
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

export const fetchAllPaymentsAsync = async (status, userId) => {
    try {
        let { data } = await getApiCall(allPaymentsAPI(userId, status));
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
export const fetchUserPaymentsAsync = async (status, userId) => {
    try {
        let { data } = await getApiCall(userPaymentsAPI(userId, status));
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

export const updateSinglePaymentAsync = async (userId, agentId, payment_id) => {
    try {
        let { data } = await putApiCall(singlePaymentAPI(userId, agentId), {
            payment_id,
        });
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
