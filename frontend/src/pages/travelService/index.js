import "./travelService.scss";
import Table from "react-bootstrap/Table";
import { useDispatch, useSelector } from "react-redux";
import Header from "../../components/header/Header";
import { ADMIN } from "../../constants/user_roles";
import add from "../../icons/add-secondary.svg";
import Button from "../../components/button/Button";
import { ADD_SERVICE_URL } from "../../constants/route_urls";
import { useNavigate } from "react-router-dom";
import { fetchTravelServicesAsync } from "../../api/travelServiceApi";
import { useEffect, useState } from "react";
import { updateServiceList } from "../../redux/travelServices/travelServiceReducer";
import { capitalize } from "@mui/material";
import { fetchCommissionsAsync } from "../../api/commissionApi";
import { updateCommissions } from "../../redux/commissions/commissionReducer";
import { Spinner } from "react-bootstrap";
import { PAGE_HEADER_TYPE } from "../../constants/header_types";

const TravelServices = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [isLoading, setLoading] = useState(false);
    const [travelServices, commissionRates, userRole, userId] = useSelector(
        (states) => [
            states.travelServices.serviceList,
            states?.commissionRates?.commissions ?? [],
            states?.users?.userDetails?.role ?? "",
            states?.users?.userDetails?.userId,
        ]
    );

    const fetchServices = async () => {
        let commissionRes = await fetchCommissionsAsync(userId);
        if (commissionRes?.length > 0) {
            dispatch(updateCommissions(commissionRes));
        }

        let res = await fetchTravelServicesAsync();
        if (res.length > 0) {
            dispatch(updateServiceList(res));
        }
        setTimeout(() => {
            setLoading(false);
        }, 1500);
    };

    useEffect(() => {
        if (userId) {
            setLoading(true);
            fetchServices();
        }
    }, [userId]);

    const serviceColumns = ["Name", "Type", "Price", "Commission"];

    const getServiceCell = (column, serviceRow) => {
        switch (column) {
            case "Name":
                return serviceRow?.name ?? "-";
            case "Type":
                return capitalize(serviceRow?.type?.toLowerCase()) ?? "-";
            case "Price":
                return "£ " + serviceRow?.price ?? "-";

            case "Commission":
                let serviceCommission = commissionRates.find(
                    (item) =>
                        String(item.service_type).toUpperCase() ==
                        String(serviceRow?.type).toUpperCase()
                );

                let serviceCommissionRate = Number(
                    Number(serviceRow?.price) *
                        (
                            Number(serviceCommission?.commission_rate) / 100
                        ).toFixed(2)
                ).toFixed(2);
                return `£ ${serviceCommissionRate}`;
        }
    };
    const handleAddService = () => {
        navigate(ADD_SERVICE_URL);
    };
    return (
        <div className='travel-services'>
            <div className='travel-services-header'>
                <Header
                    type={PAGE_HEADER_TYPE}
                    className='travel-services-title'>
                    Travel Services
                </Header>
                {userRole === ADMIN && (
                    <Button
                        type='button'
                        variant='primary'
                        className='travel-services-add'
                        fontType='fW600 fS18 secondary'
                        onClick={handleAddService}
                        preIcon={add}>
                        Add Service
                    </Button>
                )}
            </div>
            <div className='travel-services-body'>
                {isLoading ? (
                    <Spinner />
                ) : (
                    <Table striped bordered className='travel-services-table'>
                        <thead>
                            <tr>
                                {serviceColumns.map((service, key) => (
                                    <th
                                        key={`${key}-service-head`}
                                        className='travel-services-column-head'>
                                        <Header
                                            type='fS21 tertiary fW600'
                                            className='travel-services-column'>
                                            {service}
                                        </Header>
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {travelServices.length <= 0 ? (
                                <tr>
                                    <td colSpan={4}>
                                        <Header
                                            type='fW600 fS28 primary'
                                            className='travel-services-empty-row'>
                                            {userRole == ADMIN
                                                ? "You have not added any services."
                                                : "There are no services."}
                                        </Header>
                                    </td>
                                </tr>
                            ) : (
                                travelServices.map((service, key) => (
                                    <tr
                                        key={`${key}-tr-service`}
                                        className='travel-services-row'>
                                        {serviceColumns.map((item, cellKey) => (
                                            <td
                                                className='travel-services-cell'
                                                key={`${key}${cellKey}-ts-cell`}>
                                                <Header type='fW400 fS18 tertiary'>
                                                    {getServiceCell(
                                                        item,
                                                        service
                                                    )}
                                                </Header>
                                            </td>
                                        ))}
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </Table>
                )}
            </div>
        </div>
    );
};

export default TravelServices;
