import TravelAgentServiceSales from "./TravelAgentServiceSales";
import ServiceSales from "./ServiceSales";
import BookingSalesChart from "./BookingSalesChart";
import ServiceCommissions from "./ServiceCommissions";
import { useDispatch, useSelector } from "react-redux";
import { useState, useEffect } from "react";
import { ADMIN } from "../../constants/user_roles";
import { Spinner } from "react-bootstrap";
import Header from "../../components/header/Header";
import { PAGE_HEADER_TYPE } from "../../constants/header_types";
import "./home.scss";
import { fetchTravelServicesAsync } from "../../api/travelServiceApi";
import { updateServiceList } from "../../redux/travelServices/travelServiceReducer";

const Home = () => {
    const dispatch = useDispatch();
    const [userName, travelServices] = useSelector((states) => [
        states?.users?.userDetails?.name,
        states?.travelServices?.serviceList ?? [],
    ]);

    const setupHome = async () => {
        let travelServiceRes = await fetchTravelServicesAsync();
        dispatch(updateServiceList(travelServiceRes));
    };

    useEffect(() => {
        setupHome();
    }, []);

    return (
        <div className='home'>
            <div className='home-header'>
                <Header type={PAGE_HEADER_TYPE}>
                    Welcome {userName ?? ""},
                </Header>
            </div>
            <div className='home-sales-graph'>
                <TravelAgentServiceSales travelServices={travelServices} />
                <BookingSalesChart travelServices={travelServices} />
                <ServiceSales travelServices={travelServices} />
                <ServiceCommissions travelServices={travelServices} />
            </div>
        </div>
    );
};

export default Home;
