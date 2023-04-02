import * as Yup from "yup";

export const ItinerarySchema = Yup.object().shape({
    name: Yup.string().required("Required"),
    description: Yup.string().required("Required"),
    services: Yup.array()
        .of(Yup.string().required())
        .min(1)
        .test(
            "no-empty-elements",
            "Services must not contain empty elements",
            (value) => {
                return value.every((elem) => elem.trim().length > 0);
            }
        ),
});
