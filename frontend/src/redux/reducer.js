import { combineReducers } from "@reduxjs/toolkit";
import userReducer from "./users/userReducer";
import salesReducer from "./sales/salesReducer";
import travelServiceReducer from "./travelServices/travelServiceReducer";
import commissionReducer from "./commissions/commissionReducer";
import paymentReducer from "./payments/paymentReducer";

// Combine all reducers(state) of the application into one reducer
const rootReducer = combineReducers({
    users: userReducer,
    sales: salesReducer,
    travelServices: travelServiceReducer,
    commissionRates: commissionReducer,
    payments: paymentReducer,
});

export default rootReducer;
