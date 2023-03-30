import "./addTravelService.scss";
import { Formik, useFormik } from "formik";
import { useState } from "react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import Input from "../../components/input/Input";
import { SERVICE_URL } from "../../constants/route_urls";
import Dropdown from "../../components/dropdown/Dropdown";
import { addTravelServiceAsync } from "../../api/travelServiceApi";
import { travelServiceTypes } from "../../constants/travelServiceTypes";
import { capitalize } from "@mui/material";
import TravelServiceDetailsForm from "./TravelServiceDetailsForm";
import { TravelServiceSchema } from "../../schemas/TravelServiceSchema";
import Button from "../../components/button/Button";
import Header from "../../components/header/Header";
import { Form } from "react-bootstrap";
import { PAGE_HEADER_TYPE } from "../../constants/header_types";

const AddTravelService = () => {
    const navigate = useNavigate();
    const [mainError, setError] = useState("");

    const [adminId] = useSelector((states) => [
        states?.users?.userDetails?.userId,
    ]);

    const handleAddService = async (data) => {
        let res = await addTravelServiceAsync({ data, userId: adminId });
        if (res?.data?.includes("Success")) {
            navigate(SERVICE_URL);
        } else {
            setError(res?.message);
        }
    };

    const formik = useFormik({
        initialValues: {
            name: "",
            type: "",
            price: 0,
            details: {},
        },
        onSubmit: handleAddService,
        validationSchema: TravelServiceSchema,
    });

    const handleTypeChange = (data) => {
        formik.setFieldValue("type", data?.value);
    };

    const handleDetailsUpdate = (detailKey, data) => {
        let newDetails = { ...formik.values.details, [detailKey]: data };
        formik.setFieldValue("details", newDetails);
    };

    const { errors, touched } = formik;

    return (
        <div className='add-travel-service'>
            <div className='add-travel-service-header'>
                <Header type={PAGE_HEADER_TYPE}>Travel Service Form</Header>
            </div>

            <Formik className='add-travel-service-container'>
                <form
                    className='add-travel-service-form'
                    onSubmit={formik.handleSubmit}>
                    <Form.Group className='add-travel-service-form-group'>
                        <Form.Label>
                            <Header type='fS21 fW500 tertiary'>Name</Header>
                        </Form.Label>
                        <Input
                            id='name'
                            required
                            placeholder='Service name'
                            type='text'
                            className='add-travel-service-name'
                            value={formik.values.name}
                            handleChange={formik.handleChange}
                            handleBlur={formik.handleBlur}
                            error={
                                errors?.name && touched?.name
                                    ? errors?.name
                                    : ""
                            }
                        />
                    </Form.Group>
                    <Form.Group className='add-travel-service-form-group'>
                        <Form.Label>
                            <Header type='fS21 fW500 tertiary'>Type</Header>
                        </Form.Label>
                        <Dropdown
                            value={capitalize(
                                formik.values.type
                                    ? formik.values.type.toLowerCase()
                                    : "Select service type"
                            )}
                            menu={travelServiceTypes}
                            handleChange={handleTypeChange}
                            className='add-travel-service-type'
                            error={
                                errors?.type && touched?.type
                                    ? errors?.type
                                    : ""
                            }
                        />
                    </Form.Group>
                    <Form.Group className='add-travel-service-form-group'>
                        <Form.Label>
                            <Header type='fS21 fW500 tertiary'>Price</Header>
                        </Form.Label>
                        <Input
                            required
                            type='text-number'
                            placeholder='Service price'
                            id='price'
                            className='add-travel-service-price'
                            preChar='£ '
                            value={
                                formik.values.price ? formik.values.price : ""
                            }
                            handleBlur={formik.handleBlur}
                            handleChange={(e) =>
                                formik.setFieldValue("price", e.target.value)
                            }
                            error={
                                errors?.price && touched?.price
                                    ? errors?.price
                                    : ""
                            }
                        />
                    </Form.Group>
                    {formik.values.type && (
                        <div className='add-travel-service-details'>
                            <TravelServiceDetailsForm
                                formErrors={errors}
                                formTouched={touched}
                                formValues={formik.values.details}
                                type={formik.values.type}
                                handleFormUpdate={handleDetailsUpdate}
                            />
                        </div>
                    )}
                    <div className='add-travel-service-submit'>
                        <Button
                            type='submit'
                            variant='primary'
                            fontType='fW500 fS18 secondary'>
                            Add Travel Service
                        </Button>
                    </div>
                </form>
            </Formik>
        </div>
    );
};

export default AddTravelService;
