export const travelServiceTypes = [
    { title: "Flight", data: { value: "FLIGHT" } },
    { title: "Accommodation", data: { value: "ACCOMMODATION" } },
    { title: "Transportation", data: { value: "TRANSPORTATION" } },
    { title: "Activity", data: { value: "ACTIVITY" } },
];
export const flightDetails = [
    {
        fieldType: "text",
        key: "flight",
        placeholder: "Flight number",
    },
    {
        fieldType: "text",
        key: "start_loc",
        placeholder: "Flight start location",
    },
    {
        fieldType: "text",
        placeholder: "Flight destination",
        key: "end_loc",
    },
    {
        fieldType: "text",
        placeholder: "Flight service",
        key: "service_level",
    },
    { fieldType: "datepicker", key: "start_date", placeholder: "Flight time" },
];

export const accommodationDetails = [
    {
        fieldType: "text",
        placeholder: "Accommodation location",
        key: "location",
    },
    {
        fieldType: "text",
        placeholder: "Accomodation service",
        key: "service_level",
    },
    {
        fieldType: "datepicker",
        key: "start_date",
        placeholder: "Check-in date",
    },
    { fieldType: "datepicker", key: "end_date", placeholder: "Checkout date" },
];

export const activityDetails = [
    { fieldType: "text", placeholder: "Activity location", key: "location" },
    {
        fieldType: "datepicker",
        key: "start_date",
        placeholder: "Activtity start date",
    },
    {
        fieldType: "datepicker",
        key: "end_date",
        placeholder: "Activtity end date",
    },
];

export const transportationDetails = [
    { fieldType: "text", placeholder: "Start location", key: "start_loc" },
    { fieldType: "text", placeholder: "Destination location", key: "end_loc" },
    { fieldType: "datepicker", key: "start_date", placeholder: "Start time" },
    {
        fieldType: "text",
        placeholder: "Transportation service",
        key: "service_level",
    },
];
