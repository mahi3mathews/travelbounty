import { getApiCall } from "./axiosConfig";

const TRAVEL_SERVICE_URL = "/api/v1/travel-services";

export const fetchTravelServicesAsync = async () => {
    try {
        let { data } = await getApiCall(TRAVEL_SERVICE_URL);
        return data;
    } catch (error) {
        return {
            message:
                error?.response?.data?.error ??
                error?.response?.data?.message ??
                error?.response?.data?.data,
            status: error?.response?.status,
        };
    }
};
