import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    agentServiceSales: [],
    bookingSales: [],
    serviceCommissions: {},
    serviceSales: {},
};

const salesSlice = createSlice({
    initialState,
    name: "sales",
    reducers: {
        updateAgentServiceSales: (state, action) => {
            state.agentServiceSales = action.payload;
        },
        updateBookingSales: (state, action) => {
            state.bookingSales = action.payload;
        },
        updateServiceComissions: (state, action) => {
            state.serviceCommissions = action.payload;
        },
        updateServiceSales: (state, action) => {
            state.serviceSales = action.payload;
        },
        resetSales: () => initialState,
    },
});

export const {
    updateAgentServiceSales,
    updateServiceComissions,
    updateServiceSales,
    updateBookingSales,
    resetSales,
} = salesSlice.actions;
export default salesSlice.reducer;
