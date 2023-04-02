import "./addItineraryService.scss";
import { Formik, useFormik } from "formik";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import Input from "../../components/input/Input";
import { ITINERARY_URL } from "../../constants/route_urls";
import { fetchTravelServicesAsync } from "../../api/travelServiceApi";
import { ItinerarySchema } from "../../schemas/ItinerarySchema";
import Button from "../../components/button/Button";
import Header from "../../components/header/Header";
import { Form, Spinner } from "react-bootstrap";
import { PAGE_HEADER_TYPE } from "../../constants/header_types";
import { updateServiceList } from "../../redux/travelServices/travelServiceReducer";
import ServiceCheckList from "./ServiceCheckList";
import { addItineraryAsync } from "../../api/itineraryApi";

const AddItineraryService = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [mainError, setError] = useState("");
    const [totalPrice, setTotalPrice] = useState(0);
    const [isLoading, setLoading] = useState(false);

    const [userId, serviceList] = useSelector((states) => [
        states?.users?.userDetails?.userId,
        states?.travelServices?.serviceList ?? [],
    ]);

    const setupItineraryForm = async () => {
        let res = await fetchTravelServicesAsync();
        if (res?.length > 0) {
            dispatch(updateServiceList(res));
        }
    };

    useEffect(() => {
        if (userId) {
            setupItineraryForm();
        }
    }, [userId]);

    const handleAddItinerary = async (data) => {
        setLoading(true);
        let res = await addItineraryAsync(data, userId);
        if (res?.includes("Success")) {
            navigate(ITINERARY_URL);
        } else {
            setError(res?.message);
        }
        setTimeout(() => setLoading(false), 1300);
    };

    const formik = useFormik({
        initialValues: {
            name: "",
            description: "",
            services: [],
        },
        onSubmit: handleAddItinerary,
        validationSchema: ItinerarySchema,
    });

    const handleServiceSelect = (data) => {
        let newServiceList = [...formik.values.services];
        if (newServiceList.includes(data?.id)) {
            newServiceList = newServiceList.filter(
                (service) => service !== data?.id
            );
        } else {
            newServiceList.push(data?.id);
        }
        formik.setFieldValue("services", newServiceList);
        let totalAmt = 0;
        serviceList.forEach((item) =>
            newServiceList.includes(item?.id)
                ? (totalAmt += Number(item?.price))
                : null
        );
        setTotalPrice(totalAmt);
    };

    const { errors, touched } = formik;

    return (
        <div className='add-itinerary-service'>
            <div className='add-itinerary-service-header'>
                <Header type={PAGE_HEADER_TYPE}>Itinerary Form</Header>
            </div>

            <Formik className='add-itinerary-service-container'>
                <form
                    className='add-itinerary-service-form'
                    onSubmit={formik.handleSubmit}>
                    <Form.Group className='add-itinerary-service-form-group'>
                        <Form.Label>
                            <Header type='fS21 fW500 tertiary'>Name</Header>
                        </Form.Label>
                        <Input
                            id='name'
                            required
                            variant='tertiary'
                            placeholder='Itinerary name'
                            type='text'
                            className='add-itinerary-service-name'
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
                    <Form.Group className='add-itinerary-service-form-group'>
                        <Form.Label>
                            <Header type='fS21 fW500 tertiary'>
                                Description
                            </Header>
                        </Form.Label>
                        <Input
                            id='description'
                            required
                            variant='tertiary'
                            placeholder='Itinerary description'
                            type='text'
                            className='add-itinerary-service-description'
                            value={formik.values.description}
                            handleChange={formik.handleChange}
                            handleBlur={formik.handleBlur}
                            error={
                                errors?.description && touched?.description
                                    ? errors?.description
                                    : ""
                            }
                        />
                    </Form.Group>

                    <Form.Group className='add-itinerary-service-form-group'>
                        <Form.Label>
                            <Header type='fS21 fW500 tertiary'>Services</Header>
                        </Form.Label>
                        <ServiceCheckList
                            handleCheckClick={handleServiceSelect}
                            checkedList={formik.values.services}
                            services={serviceList}
                            className='add-itinerary-service-checklist'
                        />
                    </Form.Group>
                    <Form.Group className='add-itinerary-service-form-group price'>
                        <Form.Label>
                            <Header type='fS21 fW500 tertiary'>Price</Header>
                        </Form.Label>
                        <Header type='fS24 fW600 tertiary'>
                            £ {totalPrice}
                        </Header>
                    </Form.Group>
                    <div className='add-itinerary-service-submit'>
                        {isLoading ? (
                            <Spinner color='#0c8346' />
                        ) : (
                            <Button
                                type='submit'
                                variant='primary'
                                fontType='fW600 fS18 secondary'>
                                Add Itinerary
                            </Button>
                        )}
                    </div>
                </form>
            </Formik>
        </div>
    );
};

export default AddItineraryService;
