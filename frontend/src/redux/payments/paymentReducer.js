import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    paidPayments: [],
    unpaidPayments: [],
};

const paymentsSlice = createSlice({
    initialState,
    name: "payments",
    reducers: {
        updateUnpaidPayments: (state, action) => {
            state.unpaidPayments = action.payload;
        },
        updatePaidPayments: (state, action) => {
            state.paidPayments = action.payload;
        },
        resetPayments: () => initialState,
    },
});

export const { updatePaidPayments, updateUnpaidPayments, resetPayments } =
    paymentsSlice.actions;
export default paymentsSlice.reducer;
