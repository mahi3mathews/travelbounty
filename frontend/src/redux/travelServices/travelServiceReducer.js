import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    serviceList: [],
    serviceDetails: {},
};

const travelServiceSlice = createSlice({
    initialState,
    name: "travelServices",
    reducers: {
        updateServiceList: (state, action) => {
            state.serviceList = action.payload;
        },
        updateServiceDetails: (state, action) => {
            state.serviceDetails = action.payload;
        },
        resetTravelService: () => initialState,
    },
});

export const { updateServiceDetails, updateServiceList, resetTravelService } =
    travelServiceSlice.actions;
export default travelServiceSlice.reducer;
