import * as Yup from "yup";
import { travelServiceTypes } from "../constants/travelServiceTypes";

export const TravelServiceSchema = Yup.object().shape({
    name: Yup.string().required("Required"),
    price: Yup.number()
        .min(10, "Price should be minimum 10 pounds")
        .required("Required"),
    type: Yup.string()
        .oneOf(
            travelServiceTypes.map((item) => item?.data?.value),
            "Invalid value"
        )
        .required("Required"),
    details: Yup.lazy((value) => {
        if (value && value.type === "FLIGHT") {
            return Yup.object().shape({
                flight: Yup.string().required(),
                start_loc: Yup.string().required(),
                end_loc: Yup.string().required(),
                service_level: Yup.string().required(),
                start_date: Yup.date().required(),
            });
        } else if (value && value.type === "TRANSPORTATION") {
            return Yup.object().shape({
                start_loc: Yup.string().required(),
                end_loc: Yup.string().required(),
                service_level: Yup.string().required(),
                start_date: Yup.date().required(),
            });
        } else if (value && value.type === "ACTIVITY") {
            return Yup.object().shape({
                location: Yup.string().required(),
                start_date: Yup.date().required(),
                end_date: Yup.date().required(),
            });
        } else if (value && value.type === "ACCOMMODATION") {
            return Yup.object().shape({
                location: Yup.string().required(),
                service_level: Yup.string().required(),
                start_date: Yup.date().required(),
                end_date: Yup.date().required(),
            });
        } else return Yup.object();
    }),
});
