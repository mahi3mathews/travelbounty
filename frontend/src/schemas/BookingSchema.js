import * as Yup from "yup";

export const BookingSchema = Yup.object().shape({
    booking_date: Yup.date()
        .min(new Date(), "Booking date cannot be older than today.")
        .required("Required"),
    itinerary_id: Yup.string().required(
        "Please select an itinerary. It is required."
    ),
    payment_type: Yup.string().required("Required"),
    client_info: Yup.object().shape({
        name: Yup.string()
            .matches(
                /^[a-zA-Z\s]*$/,
                "Name must only contain letters and spaces"
            )
            .required("Client name is required"),
        phone_number: Yup.string()
            .matches(/^[0-9]*$/, "Phone number must only contain numbers")
            .required("Client mobile number is required"),
        email: Yup.string()
            .email("Invalid email format")
            .required("Client email is required"),
        age: Yup.number()
            .integer()
            .min(18, "Age must be over 18.")
            .required("Client age is required"),
    }),
});
