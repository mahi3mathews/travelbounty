import { configureStore } from "@reduxjs/toolkit";
import rootReducer from "./reducer";
import { createLogger } from "redux-logger";

const middleware = [];

// Redux logger to view different actions made to edit the store container
// middleware.push(createLogger());

// The state container provides the state to the application
const store = configureStore({
    reducer: rootReducer,
    middleware,
});

export default store;
