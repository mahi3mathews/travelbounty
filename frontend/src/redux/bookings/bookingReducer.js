import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    bookingList: [],
};

const bookingSlice = createSlice({
    initialState,
    name: "bookings",
    reducers: {
        updateBookings: (state, action) => {
            state.bookingList = action.payload;
        },
        resetBookings: () => initialState,
    },
});

export const { updateBookings, resetBookings } = bookingSlice.actions;
export default bookingSlice.reducer;
