import "./bookingServices.scss";

import { useEffect, useState } from "react";
import { Spinner } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { fetchBookingListAsync } from "../../api/bookingsApi";
import Button from "../../components/button/Button";
import Card from "../../components/card/Card";
import Header from "../../components/header/Header";
import { PAGE_HEADER_TYPE } from "../../constants/header_types";
import {
    BOOKING_DETAILS_URL,
    ADD_BOOKING_URL,
} from "../../constants/route_urls";
import { updateBookings } from "../../redux/bookings/bookingReducer";
import add from "../../icons/add-secondary.svg";
import { capitalize } from "@mui/material";

const BookingServices = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [userId, bookings] = useSelector((states) => [
        states?.users?.userDetails?.userId,
        states?.bookings?.bookingList ?? [],
    ]);

    const [isLoading, setLoading] = useState(false);

    const setupBooking = async () => {
        let res = await fetchBookingListAsync(userId);
        if (!res?.status) dispatch(updateBookings(res));
        setTimeout(() => setLoading(false), 1500);
    };

    const handleAddBooking = () => {
        navigate(ADD_BOOKING_URL);
    };

    const handleBookingClick = (bookingId) => {
        navigate(`${BOOKING_DETAILS_URL}/${bookingId}`);
    };
    useEffect(() => {
        if (userId) {
            if (bookings?.length <= 0) setLoading(true);
            setupBooking();
        }
    }, [userId]);
    return (
        <div className='booking-service'>
            <div className='booking-service-header'>
                <Header type={PAGE_HEADER_TYPE}>Bookings</Header>
                <Button
                    variant='primary'
                    fontType='fW600 fS18 secondary'
                    preIcon={add}
                    onClick={handleAddBooking}>
                    Add Booking
                </Button>
            </div>
            <div className='booking-service-body'>
                {isLoading ? (
                    <div className='booking-service-body-spinner'>
                        <Spinner />
                    </div>
                ) : bookings?.length <= 0 ? (
                    <Header
                        type='fS32 fW500 tertiary'
                        className='booking-service-body-empty'>
                        There are no bookings.
                    </Header>
                ) : (
                    <div className='booking-service-list'>
                        {bookings.map((item, key) => {
                            return (
                                <div
                                    key={`${key}-booking`}
                                    className='booking-service-card-container'>
                                    <Card
                                        className='booking-service-card'
                                        onClick={() =>
                                            handleBookingClick(item?.id)
                                        }>
                                        <div className='booking-service-card-header'>
                                            <Header type='fS21 fW500 secondary'>
                                                {item?.client_info?.name}
                                            </Header>
                                            <Header
                                                type={`fS24 fW600 ${
                                                    item?.status === "PAID"
                                                        ? "primary"
                                                        : "error"
                                                }`}>
                                                {capitalize(
                                                    (
                                                        item?.status ?? ""
                                                    ).toLowerCase()
                                                )}
                                            </Header>
                                        </div>
                                        <div className='booking-service-card-body'>
                                            <Header type='fS18 fW500 secondary'>
                                                {item?.client_info?.email}
                                            </Header>
                                            <Header type='fS18 fW500 secondary'>
                                                {
                                                    item?.client_info
                                                        ?.phone_number
                                                }
                                            </Header>
                                        </div>
                                        <div className='booking-service-card-booking'>
                                            <Header type='fS18 fW500 secondary'>
                                                Booking date:
                                            </Header>
                                            <Header type='fS21 fW500 secondary'>
                                                {new Date(
                                                    item?.booking_date
                                                ).toLocaleDateString("en-US", {
                                                    year: "numeric",
                                                    month: "short",
                                                    day: "numeric",
                                                })}
                                            </Header>
                                        </div>
                                        <Card className='booking-service-card-footer'>
                                            <div className='booking-service-card-footer-content'>
                                                <Header type='fS18 fW600 tertiary'>
                                                    Total Price:
                                                </Header>
                                                <Header type='fS21 fW600 secondary'>
                                                    £ {item?.total_price}
                                                </Header>
                                            </div>
                                            <div className='booking-service-card-footer-content'>
                                                <Header type='fS18 fW600 tertiary'>
                                                    Commission:
                                                </Header>
                                                <Header type='fS21 fW600 secondary'>
                                                    £ {item?.total_commission}
                                                </Header>
                                            </div>
                                        </Card>
                                    </Card>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
};

export default BookingServices;
