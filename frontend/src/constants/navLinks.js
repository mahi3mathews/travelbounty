import home from "../icons/home.svg";
import itinerary from "../icons/itinerary.svg";
import commission from "../icons/commission.svg";
import booking from "../icons/booking.svg";
import agents from "../icons/agents.svg";
import payments from "../icons/payments.svg";
import travel_services from "../icons/travel-service.svg";
import logout from "../icons/logout.svg";
import {
    HOME_URL,
    COMMISSIONS_URL,
    PAYMENTS_URL,
    BOOKING_URL,
    ITINERARY_URL,
    SERVICE_URL,
    AGENTS_URL,
    LOGOUT_URL,
    ADD_SERVICE_URL,
} from "./route_urls";
import { ADMIN, AGENT } from "./user_roles";

export const navLinks = [
    { link: HOME_URL, title: "Home", img: home, roles: [ADMIN, AGENT] },
    { link: AGENTS_URL, title: "Travel Agents", img: agents, roles: [ADMIN] },
    {
        link: ADD_SERVICE_URL,
        title: "Add Service",
        isNotNav: true,
        roles: [ADMIN],
    },
    {
        link: SERVICE_URL,
        title: "Travel Services",
        img: travel_services,
        roles: [ADMIN, AGENT],
    },
    {
        link: ITINERARY_URL,
        title: "Itineraries",
        img: itinerary,
        roles: [AGENT],
    },
    {
        link: BOOKING_URL,
        title: "Bookings",
        img: booking,
        roles: [AGENT],
    },
    {
        link: PAYMENTS_URL,
        title: "Payments",
        img: payments,
        roles: [ADMIN, AGENT],
    },
    {
        link: COMMISSIONS_URL,
        title: "Commissions",
        img: commission,
        roles: [ADMIN],
    },
    {
        link: LOGOUT_URL,
        title: "Logout",
        img: logout,
        roles: [ADMIN, AGENT],
    },
];
