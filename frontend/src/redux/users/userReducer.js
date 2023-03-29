import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    agents: [],
    userDetails: {},
};

const userSlice = createSlice({
    initialState,
    name: "users",
    reducers: {
        setAgentUsers: (state, action) => {
            state.agents = action.payload;
        },
        updateAgentUsers: (state, action) => {
            state.agents.push(action.payload);
        },
        setUserDetails: (state, action) => {
            state.userDetails = action.payload;
        },
        updateUserDetails: (state, action) => {
            state.userDetails = { ...state.userDetails, ...action.payload };
        },
        resetUser: () => initialState,
    },
});

export const {
    setUserDetails,
    updateUserDetails,
    resetUser,
    setAgentUsers,
    updateAgentUsers,
} = userSlice.actions;
export default userSlice.reducer;
