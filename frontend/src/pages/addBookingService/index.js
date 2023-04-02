import { capitalize } from "@mui/material";
import { Formik, useFormik } from "formik";
import { useEffect, useState } from "react";
import { Alert, Form } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { addBookingAsync } from "../../api/bookingsApi";
import { fetchItineraryListAsync } from "../../api/itineraryApi";
import Button from "../../components/button/Button";
import DatePicker from "../../components/datepicker/Datepicker";
import Dropdown from "../../components/dropdown/Dropdown";
import Header from "../../components/header/Header";
import Icon from "../../components/icon/Icon";
import Input from "../../components/input/Input";
import { PAGE_HEADER_TYPE } from "../../constants/header_types";
import { BOOKING_URL } from "../../constants/route_urls";
import { updateItineraries } from "../../redux/itinerary/itineraryReducer";
import { BookingSchema } from "../../schemas/BookingSchema";
import ServiceCheckList from "../addItineraryService/ServiceCheckList";
import chevDown from "../../icons/chev-down-tertiary.svg";
import "./addBooking.scss";

const AddBookingService = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const [userId, itineraries] = useSelector((states) => [
        states?.users?.userDetails?.userId,
        states?.itinerary?.itineraries ?? [],
    ]);
    const [error, setError] = useState("");
    const [isLoading, setLoading] = useState(false);
    const [showClientSection, setShowClient] = useState(false);
    const [totalPrice, setTotalPrice] = useState(0.0);

    const paymentMenu = [
        { title: "Card", data: { value: "CARD" } },
        { title: "Online", data: { value: "ONLINE" } },
        { title: "Cash", data: { value: "CASH" } },
    ];

    const setupBookingForm = async () => {
        let res = await fetchItineraryListAsync(userId);
        dispatch(updateItineraries(res));
        setTimeout(() => setLoading(false), 1500);
    };

    useEffect(() => {
        if (userId) {
            setLoading(true);
            setupBookingForm();
        }
    }, [userId]);

    const handleAddBooking = async (data) => {
        let res = await addBookingAsync(data, userId);
        if (res?.includes("Success")) {
            navigate(BOOKING_URL);
        } else {
            setError(res?.message);
        }
        setTimeout(() => setLoading(false), 1300);
    };

    const formik = useFormik({
        initialValues: {
            booking_date: "",
            itinerary_id: "",
            client_info: {
                name: "",
                email: "",
                phone_number: "",
                age: 18,
            },
            payment_type: "",
        },
        onSubmit: handleAddBooking,
        validationSchema: BookingSchema,
    });
    const { errors, touched } = formik;

    const handleErrorCheck = () => {
        let errKeys = Object.keys(errors);
        if (errKeys?.length > 0) {
            if (errKeys[0] === "client_info") {
                setError(Object.values(errors.client_info)[0]);
            } else {
                setError(errors[errKeys[0]]);
            }
        } else {
            setError("");
        }
    };

    const handleItinerarySelect = (item) => {
        formik.setFieldValue("itinerary_id", item?.id);
        setTotalPrice(item?.total_price);
        setError("");
    };

    const handlePaymentChange = (data) => {
        formik.setFieldValue("payment_type", data?.value);
    };

    const handleBookingDateChange = (value) => {
        formik.setFieldValue("booking_date", value);
    };

    return (
        <div className='add-booking-service'>
            <div className='add-booking-service-header'>
                <Header type={PAGE_HEADER_TYPE}>Booking Form</Header>
            </div>
            <div className='add-booking-service-alert'>
                {error && (
                    <Alert
                        variant='danger'
                        onClose={() => setError("")}
                        dismissible>
                        {error}
                    </Alert>
                )}
            </div>
            <div className='add-booking-service-body'>
                <Formik className='add-booking-service-formik'>
                    <form
                        className='add-booking-service-form'
                        onSubmit={(e) => {
                            formik.handleSubmit(e);
                            handleErrorCheck();
                        }}>
                        <div className='add-booking-service-booking'>
                            <Header
                                type='fS24 fW600 tertiary'
                                className='add-booking-service-booking-title'>
                                Booking details:
                            </Header>
                            <Form.Group className='add-booking-service-group'>
                                <Form.Label>
                                    <Header type='fW500 fS21 tertiary'>
                                        Date
                                    </Header>
                                </Form.Label>
                                <DatePicker
                                    minDate={new Date()}
                                    value={formik?.values?.booking_date ?? ""}
                                    placeholderText='Booking date'
                                    className='add-booking-service-booking-date'
                                    handleChange={handleBookingDateChange}
                                    error={errors.booking_date}
                                />
                            </Form.Group>
                            <Form.Group className='add-booking-service-group'>
                                <Form.Label>
                                    <Header type='fW500 fS21 tertiary'>
                                        Itinerary
                                    </Header>
                                </Form.Label>
                                <ServiceCheckList
                                    className='add-booking-service-itinerary'
                                    handleCheckClick={handleItinerarySelect}
                                    services={itineraries}
                                    checkedList={[formik.values.itinerary_id]}
                                />
                                <div className='add-booking-service-itinerary-total-price'>
                                    <Header type='fW600 fS18 primary'>
                                        Total Price:
                                    </Header>
                                    <Header type='fW600 fS24 primary'>
                                        £ {totalPrice}
                                    </Header>
                                </div>
                            </Form.Group>
                            <Form.Group className='add-booking-service-group'>
                                <Form.Label>
                                    <Header type='fW500 fS21 tertiary'>
                                        Payment Method
                                    </Header>
                                </Form.Label>
                                <Dropdown
                                    menu={paymentMenu}
                                    value={
                                        formik.values.payment_type
                                            ? capitalize(
                                                  formik.values?.payment_type?.toLowerCase()
                                              )
                                            : "Client payment method"
                                    }
                                    handleChange={handlePaymentChange}
                                    className='add-booking-service-payment-method'
                                    error={errors.payment_type}
                                />
                            </Form.Group>
                        </div>
                        <div className='add-booking-service-client'>
                            <div
                                className='add-booking-service-client-header'
                                onClick={() =>
                                    setShowClient((prevState) => !prevState)
                                }>
                                <Header
                                    type='fS24 fW600 tertiary'
                                    className='add-booking-service-client-title'>
                                    Client details:
                                </Header>
                                <Icon
                                    src={chevDown}
                                    className={`add-booking-service-client-arrow ${
                                        showClientSection || error
                                            ? "show"
                                            : "hide"
                                    }`}
                                />
                            </div>

                            <div
                                className={`add-booking-service-client-group ${
                                    showClientSection || error ? "show" : ""
                                }`}>
                                <Form.Group className='add-booking-service-group'>
                                    <Form.Label>
                                        <Header type='fW500 fS21 tertiary'>
                                            Name
                                        </Header>
                                    </Form.Label>
                                    <Input
                                        type='text'
                                        value={formik.values.client_info?.name}
                                        handleChange={formik.handleChange}
                                        handleBlur={formik.handleBlur}
                                        placeholder='Client name'
                                        id='client-name'
                                        name='client_info.name'
                                        error={
                                            errors?.client_info?.name &&
                                            touched?.client_info?.name
                                                ? errors?.client_info?.name
                                                : ""
                                        }
                                        className='add-booking-service-client-name'
                                    />
                                </Form.Group>
                                <Form.Group className='add-booking-service-group'>
                                    <Form.Label>
                                        <Header type='fW500 fS21 tertiary'>
                                            Mobile Number
                                        </Header>
                                    </Form.Label>
                                    <Input
                                        type='text-number'
                                        value={
                                            formik.values.client_info
                                                ?.phone_number
                                        }
                                        maxLength={11}
                                        handleChange={formik.handleChange}
                                        handleBlur={formik.handleBlur}
                                        placeholder='Client mobile number'
                                        id='client-number'
                                        name='client_info.phone_number'
                                        error={
                                            errors?.client_info?.phone_number &&
                                            touched?.client_info?.phone_number
                                                ? errors?.client_info
                                                      ?.phone_number
                                                : ""
                                        }
                                        className='add-booking-service-client-number'
                                    />
                                </Form.Group>
                                <Form.Group className='add-booking-service-group'>
                                    <Form.Label>
                                        <Header type='fW500 fS21 tertiary'>
                                            Email
                                        </Header>
                                    </Form.Label>
                                    <Input
                                        type='text'
                                        name='client_info.email'
                                        value={formik.values.client_info?.email}
                                        handleChange={formik.handleChange}
                                        handleBlur={formik.handleBlur}
                                        placeholder='Client email'
                                        id='client-email'
                                        error={
                                            errors?.client_info?.email &&
                                            touched?.client_info?.email
                                                ? errors?.client_info?.email
                                                : ""
                                        }
                                        className='add-booking-service-client-email'
                                    />
                                </Form.Group>
                                <Form.Group className='add-booking-service-group'>
                                    <Form.Label>
                                        <Header type='fW500 fS21 tertiary'>
                                            Age
                                        </Header>
                                    </Form.Label>
                                    <Input
                                        type='number'
                                        name='client_info.age'
                                        value={formik.values.client_info.age}
                                        handleChange={formik.handleChange}
                                        handleBlur={formik.handleBlur}
                                        placeholder='Client age'
                                        id='client-age'
                                        error={
                                            errors?.client_info?.age &&
                                            touched?.client_info?.age
                                                ? errors?.client_info?.age
                                                : ""
                                        }
                                        className='add-booking-service-client-age'
                                    />
                                </Form.Group>
                            </div>
                        </div>
                        <div className='add-booking-service-submit'>
                            <Button
                                type='submit'
                                variant='primary'
                                fontType='fS18 fW600 secondary'
                                className='add-booking-service-submit-btn'>
                                Submit
                            </Button>
                        </div>
                    </form>
                </Formik>
            </div>
        </div>
    );
};

export default AddBookingService;
