import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    commissions: [],
};

const commissionSlice = createSlice({
    initialState,
    name: "commissionRates",
    reducers: {
        updateCommissions: (state, action) => {
            state.commissions = action.payload;
        },
        resetCommissions: () => initialState,
    },
});

export const { updateCommissions, resetCommissions } = commissionSlice.actions;
export default commissionSlice.reducer;
