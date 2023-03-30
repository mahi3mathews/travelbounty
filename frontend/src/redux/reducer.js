import { combineReducers } from "@reduxjs/toolkit";
import userReducer from "./users/userReducer";
import salesReducer from "./sales/salesReducer";
import travelServiceReducer from "./travelServices/travelServiceReducer";
import commissionReducer from "./commissions/commissionReducer";

// Combine all reducers(state) of the application into one reducer
const rootReducer = combineReducers({
    users: userReducer,
    sales: salesReducer,
    travelServices: travelServiceReducer,
    commissionRates: commissionReducer,
});

export default rootReducer;
