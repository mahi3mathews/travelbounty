import { getApiCall, putApiCall } from "./axiosConfig";

const adminCommissionAPI = (adminId) => `/api/v1/${adminId}/commissions`;
const updateCommissionAPI = (adminId, commissionId) =>
    `${adminCommissionAPI(adminId)}/${commissionId}`;

export const fetchCommissionsAsync = async (userId) => {
    try {
        let { data } = await getApiCall(adminCommissionAPI(userId));
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

export const updateCommissionRateAsync = async (
    payload,
    commissionId,
    userId
) => {
    try {
        let { data } = await putApiCall(
            updateCommissionAPI(userId, commissionId),
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
