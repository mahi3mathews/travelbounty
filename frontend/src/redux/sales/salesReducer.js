import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    agentServiceSales: [],
};

const salesSlice = createSlice({
    initialState,
    name: "sales",
    reducers: {
        updateAgentServiceSales: (state, action) => {
            state.agentServiceSales = action.payload;
        },
        resetSales: () => initialState,
    },
});

export const { updateAgentServiceSales, resetSales } = salesSlice.actions;
export default salesSlice.reducer;
