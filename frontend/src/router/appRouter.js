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
    BOOKING_DETAILS_URL,
    ITINERARY_DETAILS_URL,
    SERVICE_DETAILS_URL,
    AGENT_DETAILS_URL,
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
import AddTravelService from "../pages/addTravelService";
import TravelAgents from "../pages/travelAgents";
import CommissionRates from "../pages/commissionRates";
import BookingServices from "../pages/bookingServices";
import ItineraryServices from "../pages/itineraryService";
import AddBookingService from "../pages/addBookingService";
import AddItineraryService from "../pages/addItineraryService";
import AgentDetails from "../pages/agentDetails";
import Payments from "../pages/payments";

const AppRouter = ({}) => {
    const navigate = useNavigate();
    const location = useLocation();
    const [isLoading, setLoading] = useState(true);
    const [userRole] = useSelector((states) => [
        states?.users?.userDetails?.role,
    ]);

    const componentLoader = (component) => (isLoading ? null : component);

    const checkDynamicUrls = (userURL, pathname) => {
        if (pathname.includes("details")) {
        }
    };

    useEffect(() => {
        const loggedOutUrls = [LOGIN_URL, REGISTER_URL];
        const isLoggedIn = localStorage.getItem("isUserLoggedIn") === "true";
        const adminUrls = navLinks
            .filter((link) => link.roles.includes(ADMIN))
            .map((link) => link.link);
        const agentUrls = navLinks
            .filter((link) => link.roles.includes(AGENT))
            .map((link) => link.link);
        if (!isLoggedIn && !loggedOutUrls.includes(location.pathname)) {
            navigate(LOGIN_URL);
        } else if (isLoggedIn && loggedOutUrls.includes(location.pathname)) {
            navigate(HOME_URL);
        } else if (
            isLoggedIn &&
            userRole === ADMIN &&
            !adminUrls.some(
                (link) =>
                    link.startsWith(location.pathname) ||
                    location.pathname.startsWith(link)
            )
        ) {
            // Case-scenario where admin tries to access links not provided to them
            navigate(HOME_URL);
        } else if (
            isLoggedIn &&
            userRole === AGENT &&
            !agentUrls.some(
                (link) =>
                    link.startsWith(location.pathname) ||
                    location.pathname.startsWith(link)
            )
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
            <Route
                path={ADD_SERVICE_URL}
                element={componentLoader(<AddTravelService />)}
            />
            <Route
                path={AGENTS_URL}
                element={componentLoader(<TravelAgents />)}
            />
            <Route
                path={`${AGENT_DETAILS_URL}/:id`}
                element={componentLoader(<AgentDetails />)}
            />
            <Route
                path={COMMISSIONS_URL}
                element={componentLoader(<CommissionRates />)}
            />
            <Route
                path={BOOKING_URL}
                element={componentLoader(<BookingServices />)}
            />
            <Route
                path={ITINERARY_URL}
                element={componentLoader(<ItineraryServices />)}
            />
            <Route
                path={`${BOOKING_DETAILS_URL}/:id`}
                element={componentLoader(<BookingServices />)}
            />
            <Route
                path={`${ITINERARY_DETAILS_URL}/:id`}
                element={componentLoader(<ItineraryServices />)}
            />
            <Route
                path={ADD_BOOKING_URL}
                element={componentLoader(<AddBookingService />)}
            />
            <Route
                path={ADD_ITINERARY_URL}
                element={componentLoader(<AddItineraryService />)}
            />
            <Route
                path={PAYMENTS_URL}
                element={componentLoader(<Payments />)}
            />
        </Routes>
    );
};

export default AppRouter;
