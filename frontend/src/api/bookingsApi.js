import { deleteApiCall, getApiCall, postApiCall } from "./axiosConfig";

const AGENT_SERVICE_API = "/api/v1/agent-services";

export const addBookingAsync = async (payload, userId) => {
    try {
        let { data } = await postApiCall(AGENT_SERVICE_API, {
            data: { ...payload, agent_id: userId },
            service_type: "booking",
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

export const fetchBookingListAsync = async (userId) => {
    try {
        let { data } = await getApiCall(
            `${AGENT_SERVICE_API}?type=booking&agent=${userId}`
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

export const fetchBookingDetailsAsync = async (serviceId, userId) => {
    try {
        let { data } = await getApiCall(
            `${AGENT_SERVICE_API}/${serviceId}?type=booking&agent=${userId}`
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

export const removeBookingAsync = async (serviceId, userId) => {
    try {
        let { data } = await deleteApiCall(
            `${AGENT_SERVICE_API}/${serviceId}?type=booking&agent=${userId}`
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
