import { useEffect, useState } from "react";
import { Spinner } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { fetchItineraryListAsync } from "../../api/itineraryApi";
import Button from "../../components/button/Button";
import Card from "../../components/card/Card";
import Header from "../../components/header/Header";
import { PAGE_HEADER_TYPE } from "../../constants/header_types";
import {
    ADD_ITINERARY_URL,
    ITINERARY_DETAILS_URL,
} from "../../constants/route_urls";
import { updateItineraries } from "../../redux/itinerary/itineraryReducer";
import "./itineraryService.scss";
import add from "../../icons/add-secondary.svg";

const ItineraryServices = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [userId, itineraries] = useSelector((states) => [
        states?.users?.userDetails?.userId,
        states?.itinerary?.itineraries,
    ]);

    const [isLoading, setLoading] = useState(false);

    const setupItinerary = async () => {
        let res = await fetchItineraryListAsync(userId);
        dispatch(updateItineraries(res));
        setTimeout(() => setLoading(false), 1500);
    };

    const handleAddItinerary = () => {
        navigate(ADD_ITINERARY_URL);
    };

    const handleItineraryClick = (itineraryId) => {
        navigate(`${ITINERARY_DETAILS_URL}/${itineraryId}`);
    };
    useEffect(() => {
        if (userId) {
            if (itineraries?.length <= 0) setLoading(true);
            setupItinerary();
        }
    }, [userId]);
    return (
        <div className='itinerary-service'>
            <div className='itinerary-service-header'>
                <Header type={PAGE_HEADER_TYPE}>Itineraries</Header>
                <Button
                    variant='primary'
                    fontType='fW600 fS18 secondary'
                    preIcon={add}
                    onClick={handleAddItinerary}>
                    Add Itinerary
                </Button>
            </div>
            <div className='itinerary-service-body'>
                {isLoading ? (
                    <Spinner />
                ) : itineraries?.length <= 0 ? (
                    <Header
                        type='fS32 fW500 tertiary'
                        className='booking-service-body-empty'>
                        There are no itineraries.
                    </Header>
                ) : (
                    <div className='itinerary-service-list'>
                        {itineraries.map((item, key) => {
                            return (
                                <div
                                    key={`${key}-itinerary`}
                                    className='itinerary-service-card-container'>
                                    <Card
                                        className='itinerary-service-card'
                                        onClick={() =>
                                            handleItineraryClick(item?.id)
                                        }>
                                        <div className='itinerary-service-card-header'>
                                            <Header type='fS21 fW500 secondary'>
                                                {item?.name}
                                            </Header>
                                            <Header type='fS24 fW500 secondary'>
                                                £ {item?.total_price}
                                            </Header>
                                        </div>
                                        <div className='itinerary-service-card-body'>
                                            <Header type='fS18 fW500 secondary'>
                                                {item?.description}
                                            </Header>
                                        </div>
                                        <Card className='itinerary-service-card-footer'>
                                            <Header type='fS18 fW600 tertiary'>
                                                Commission:
                                            </Header>
                                            <Header type='fS21 fW600 secondary'>
                                                £ {item?.total_commission}
                                            </Header>
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

export default ItineraryServices;
