import { getApiCall } from "./axiosConfig";

const BASE_API_URL = "/api/v1";
const adminTravelServiceSalesApi = (adminId) =>
    `${BASE_API_URL}/${adminId}/agents/service-sales`;

export const travelAgentServiceSalesAsync = async (adminId) => {
    try {
        let { data } = await getApiCall(adminTravelServiceSalesApi(adminId));
        console.log(data, "DATA");
        return data;
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
