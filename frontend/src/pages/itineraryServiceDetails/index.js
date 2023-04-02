import { useEffect, useState } from "react";
import { Spinner } from "react-bootstrap";
import { useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { fetchItineraryDetailsAsync } from "../../api/itineraryApi";
import Header from "../../components/header/Header";
import { PAGE_HEADER_TYPE } from "../../constants/header_types";
import ServiceCheckList from "../addItineraryService/ServiceCheckList";
import "./itineraryServiceDetails.scss";

const ItineraryServiceDetails = () => {
    const { id } = useParams();
    const [userId] = useSelector((states) => [
        states?.users?.userDetails?.userId,
    ]);
    const [isLoading, setLoading] = useState(false);
    const [itineraryDetails, setItineraryDetails] = useState({});
    const setupItineraryDetails = async () => {
        let res = await fetchItineraryDetailsAsync(id, userId);
        setItineraryDetails(res);
        setTimeout(() => setLoading(false), 1500);
    };
    useEffect(() => {
        if (userId) {
            setLoading(true);
            setupItineraryDetails();
        }
    }, [userId]);
    return (
        <div className='itinerary-service-details'>
            <div className='itinerary-service-details-header'>
                <Header type={PAGE_HEADER_TYPE}>Itinerary Details</Header>
            </div>
            <div className='itinerary-service-details-body'>
                {isLoading ? (
                    <Spinner />
                ) : Object.keys(itineraryDetails)?.length > 0 ? (
                    <div className='itinerary-service-details-container'>
                        <div className='itinerary-service-details-name'>
                            <Header type='fS24 fW500 tertiary'>
                                {itineraryDetails?.name}
                            </Header>
                        </div>
                        <div className='itinerary-service-details-description'>
                            <Header type='fS18 fW500 tertiary'>
                                {itineraryDetails?.description}
                            </Header>
                        </div>
                        <div className='itinerary-service-details-services'>
                            <ServiceCheckList
                                services={itineraryDetails?.services}
                                allChecked
                                checkDisabled
                                className='itinerary-service-details-service-list'
                            />
                        </div>
                        <div className='itinerary-service-details-commission'>
                            <Header type='fS18 fW600 tertiary'>
                                Total commission:
                            </Header>
                            <Header type='fS21 fW600 tertiary'>
                                £ {itineraryDetails?.total_commission}
                            </Header>
                        </div>
                        <div className='itinerary-service-details-price'>
                            <Header type='fS18 fW600 tertiary'>
                                Total price:
                            </Header>
                            <Header type='fS21 fW600 tertiary'>
                                £ {itineraryDetails?.total_price}
                            </Header>
                        </div>
                    </div>
                ) : (
                    <div className='itinerary-service-details-empty'></div>
                )}
            </div>
        </div>
    );
};

export default ItineraryServiceDetails;
