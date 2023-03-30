import { getApiCall } from "./axiosConfig";

const adminCommissionAPI = (adminId) => `/api/v1/${adminId}/commissions`;

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
