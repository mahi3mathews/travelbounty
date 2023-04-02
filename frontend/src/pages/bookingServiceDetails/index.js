import "./bookingServiceDetails.scss";

import { useEffect, useState } from "react";
import { Badge, Spinner } from "react-bootstrap";
import { useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
import {
    fetchBookingDetailsAsync,
    removeBookingAsync,
} from "../../api/bookingsApi";
import Header from "../../components/header/Header";
import { PAGE_HEADER_TYPE } from "../../constants/header_types";
import ServiceCheckList from "../addItineraryService/ServiceCheckList";
import { capitalize } from "@mui/material";
import Button from "../../components/button/Button";
import { BOOKING_URL } from "../../constants/route_urls";

const BookingServiceDetails = () => {
    const navigate = useNavigate();
    const { id } = useParams();
    const [userId] = useSelector((states) => [
        states?.users?.userDetails?.userId,
    ]);
    const [isLoading, setLoading] = useState(false);
    const [bookingDetails, setBookingDetails] = useState({});

    const setupBookingDetails = async () => {
        let res = await fetchBookingDetailsAsync(id, userId);
        setBookingDetails(res);
        setTimeout(() => setLoading(false), 1500);
    };

    const handleRemoveBooking = async () => {
        let res = await removeBookingAsync(id, userId);
        if (res.includes("Success")) {
            navigate(BOOKING_URL);
        }
    };

    const handlePrintBooking = () => {
        var content = document.getElementById("booking-service-details");
        var domClone = content.cloneNode(true);
        var printSection = document.createElement("div");
        printSection.id = "printSection";
        document.body.appendChild(printSection);
        printSection.appendChild(domClone);
        var style = document.createElement("style");
        style.media = "print";
        style.innerHTML = `
          @page { size: auto;  margin: 0mm; }
          body * { visibility: hidden; }
          #printSection, #printSection * { visibility: visible; }
          #printSection { position: absolute; left: 0; top: 0; }
        `;
        document.head.appendChild(style);
        window.print();
        document.body.removeChild(printSection);
        document.head.removeChild(style);
    };
    useEffect(() => {
        if (userId) {
            setLoading(true);
            setupBookingDetails();
        }
    }, [userId]);
    return (
        <div id='booking-service-details' className='booking-service-details'>
            <div className='booking-service-details-header'>
                <Header type={PAGE_HEADER_TYPE}>Booking Details</Header>
            </div>
            <div className='booking-service-details-body'>
                {isLoading ? (
                    <Spinner />
                ) : Object.keys(bookingDetails)?.length > 0 ? (
                    <div className='booking-service-details-container'>
                        <div className='booking-service-details-date'>
                            <Header type='fS24 fW500 tertiary'>
                                Booking date:
                            </Header>
                            <Header type='fS18 fW500 tertiary'>
                                {new Date(
                                    bookingDetails?.booking_date
                                ).toLocaleDateString("en-US", {
                                    year: "numeric",
                                    month: "short",
                                    day: "numeric",
                                })}
                            </Header>
                        </div>
                        <div className='booking-service-details-status'>
                            <Header type='fS24 fW500 tertiary'>
                                Payment status:
                            </Header>
                            <Badge
                                pill
                                className='booking-service-details-name-status'
                                variant='transparent'
                                color={
                                    bookingDetails?.status === "PAID"
                                        ? "#0c8346"
                                        : "#b42e2e"
                                }>
                                {capitalize(
                                    (bookingDetails?.status ?? "").toLowerCase()
                                )}
                            </Badge>
                        </div>
                        <div className='booking-service-details-client'>
                            <Header type='fS24 fW500 tertiary'>
                                Client details:
                            </Header>
                            <div className='booking-service-details-client-details'>
                                <Header type='fS18 fW600 tertiary'>
                                    {bookingDetails?.client_info?.name}
                                </Header>
                                <Header type='fS18 fW500 tertiary'>
                                    {bookingDetails?.client_info?.email}
                                </Header>
                                <Header type='fS18 fW500 tertiary'>
                                    {bookingDetails?.client_info?.phone_number}
                                </Header>
                            </div>
                        </div>
                        <div className='booking-service-details-name'>
                            <Header type='fS24 fW500 tertiary'>
                                {bookingDetails?.itinerary_name}
                            </Header>
                        </div>

                        <div className='booking-service-details-description'>
                            <Header type='fS18 fW500 tertiary'>
                                {bookingDetails?.itinerary_description}
                            </Header>
                        </div>

                        <div className='booking-service-details-services'>
                            <ServiceCheckList
                                services={bookingDetails?.services}
                                allChecked
                                checkDisabled
                                className='booking-service-details-service-list'
                            />
                        </div>
                        <div className='booking-service-details-commission'>
                            <Header type='fS18 fW600 tertiary'>
                                Total commission earned:
                            </Header>
                            <Header type='fS21 fW600 tertiary'>
                                £ {bookingDetails?.total_commission}
                            </Header>
                        </div>
                        <div className='booking-service-details-price'>
                            <Header type='fS18 fW600 tertiary'>
                                Total price:
                            </Header>
                            <Header type='fS21 fW600 tertiary'>
                                £ {bookingDetails?.total_price}
                            </Header>
                        </div>
                        <div className='booking-service-details-footer'>
                            <Button
                                variant='primary'
                                fontType='fS18 fW600 secondary'
                                onClick={handlePrintBooking}>
                                Print
                            </Button>
                            <Button
                                variant='tertiary'
                                fontType='fS18 fW600 secondary'
                                onClick={handleRemoveBooking}>
                                Remove
                            </Button>
                        </div>
                    </div>
                ) : (
                    <div className='booking-service-details-empty'></div>
                )}
            </div>
        </div>
    );
};

export default BookingServiceDetails;
