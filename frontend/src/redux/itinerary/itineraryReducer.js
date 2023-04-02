import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    itineraries: [],
};

const itinerarySlice = createSlice({
    initialState,
    name: "itinerary",
    reducers: {
        updateItineraries: (state, action) => {
            state.itineraries = action.payload;
        },
        resetItinerary: () => initialState,
    },
});

export const { updateItineraries, resetItinerary } = itinerarySlice.actions;
export default itinerarySlice.reducer;
