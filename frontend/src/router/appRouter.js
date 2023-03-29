import {
    BOOKING_URL,
    COMMISSIONS_URL,
    ITINERARY_URL,
    SERVICE_URL,
    REGISTER_URL,
    LOGIN_URL,
    LOGOUT_URL,
    ADD_BOOKING_URL,
    ADD_ITINERARY_URL,
    ADD_SERVICE_URL,
    HOME_URL,
    PAYMENTS_URL,
    AGENTS_URL,
} from "../constants/route_urls";
import { Route, Routes, useLocation } from "react-router-dom";
import Home from "../pages/home";
import Login from "../pages/login";
import Register from "../pages/register";
import Logout from "../pages/logout";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { navLinks } from "../constants/navLinks";
import { ADMIN, AGENT } from "../constants/user_roles";
import TravelServices from "../pages/travelService";

const AppRouter = ({}) => {
    const navigate = useNavigate();
    const location = useLocation();
    const [isLoading, setLoading] = useState(true);
    const [userRole] = useSelector((states) => [
        states?.users?.userDetails?.role,
    ]);

    const componentLoader = (component) => (isLoading ? null : component);

    useEffect(() => {
        const loggedOutUrls = [LOGIN_URL, REGISTER_URL];
        const isLoggedIn = localStorage.getItem("isUserLoggedIn") == "true";
        const adminUrls = navLinks
            .filter((link) => link.roles.includes(ADMIN))
            .map((link) => link.link);
        const agentUrls = navLinks
            .filter((link) => link.roles.includes(AGENT))
            .map((link) => link.link);
        console.log(adminUrls, agentUrls, userRole, location.pathname);
        if (!isLoggedIn && !loggedOutUrls.includes(location.pathname)) {
            navigate(LOGIN_URL);
        } else if (isLoggedIn && loggedOutUrls.includes(location.pathname)) {
            navigate(HOME_URL);
        } else if (
            isLoggedIn &&
            userRole === ADMIN &&
            !adminUrls.includes(location.pathname)
        ) {
            // Case-scenario where admin tries to access links not provided to them
            navigate(HOME_URL);
        } else if (
            isLoggedIn &&
            userRole === AGENT &&
            !agentUrls.includes(location.pathname)
        ) {
            // Case-scenario where attendee tries to access links not provided to them
            navigate(HOME_URL);
        }
        setLoading(false);
    }, [location.pathname, navigate, userRole]);

    return (
        <Routes>
            <Route
                path={REGISTER_URL}
                element={componentLoader(<Register />)}
            />
            <Route path={LOGIN_URL} element={componentLoader(<Login />)} />
            <Route path={HOME_URL} element={componentLoader(<Home />)} />
            <Route path={LOGOUT_URL} element={componentLoader(<Logout />)} />
            <Route
                path={SERVICE_URL}
                element={componentLoader(<TravelServices />)}
            />
            {/* 

            
            <Route
                path={COMMISSIONS_URL}
                element={componentLoader(<AddEditCourse />)}
            />
            <Route
                path={BOOKING_URL}
                element={componentLoader(<CoursesView />)}
            />
            <Route
                path={ITINERARY_URL}
                element={componentLoader(<AddEditTraining />)}
            />
            <Route
                path={ADD_BOOKING_URL}
                element={componentLoader(<AddApplication />)}
            />
            <Route
                path={ADD_ITINERARY_URL}
                element={componentLoader(<AddEditTraining isEdit />)}
            />
            <Route
                path={ADD_SERVICE_URL}
                element={componentLoader(<AddEditCourse isEdit />)}
            /> */}
        </Routes>
    );
};

export default AppRouter;
