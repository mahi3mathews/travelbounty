import { getApiCall, postApiCall } from "./axiosConfig";

const AGENT_SERVICE_API = "/api/v1/agent-services";

export const addItineraryAsync = async (payload, userId) => {
    try {
        let { data } = await postApiCall(AGENT_SERVICE_API, {
            data: { ...payload, agent_id: userId },
            service_type: "itinerary",
        });
        return data?.data ?? data;
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

export const fetchItineraryListAsync = async (userId) => {
    try {
        let { data } = await getApiCall(
            `${AGENT_SERVICE_API}?type=itinerary&agent=${userId}`
        );
        return data?.data ?? data;
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

export const fetchItineraryDetailsAsync = async (serviceId, userId) => {
    try {
        let { data } = await getApiCall(
            `${AGENT_SERVICE_API}/${serviceId}?type=itinerary&agent=${userId}`
        );
        return data?.data ?? data;
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
