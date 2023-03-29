import { combineReducers } from "@reduxjs/toolkit";
import userReducer from "./users/userReducer";
import salesReducer from "./sales/salesReducer";
import travelServiceReducer from "./travelServices/travelServiceReducer";

// Combine all reducers(state) of the application into one reducer
const rootReducer = combineReducers({
    users: userReducer,
    sales: salesReducer,
    travelServices: travelServiceReducer,
});

export default rootReducer;
