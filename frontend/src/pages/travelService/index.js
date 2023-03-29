import "./travelService.scss";
import { Table } from "react-bootstrap";
import { useSelector } from "react-redux";
import Header from "../../components/header/Header";
import { ADMIN } from "../../constants/user_roles";

const TravelServices = () => {
    const [travelServices, commissionRates, userRole] = useSelector(
        (states) => [
            states.travelServices.serviceList,
            states?.commissionRates?.commissions ?? [],
            states?.users?.userDetails?.role ?? "",
        ]
    );

    const serviceColumns = ["Name", "Type", "Price", "Commission"];

    const getServiceCell = (column, serviceRow) => {
        switch (column) {
            case "Name":
                return serviceRow?.name ?? "-";
            case "Type":
                return serviceRow?.type ?? "-";
            case "Price":
                return "£" + serviceRow?.price ?? "-";

            case "Commission":
                let serviceCommission = commissionRates.find(
                    (item) =>
                        String(item.type).toUpperCase() ==
                        String(serviceRow?.type).toUpperCase()
                );
                let serviceCommissionRate = Number(
                    Number(serviceRow?.price) *
                        (
                            Number(serviceCommission?.commissionRate) / 100
                        ).toFixed(2)
                ).toFixed(2);
                return `£${serviceCommissionRate}`;
        }
    };
    return (
        <div className='travel-services'>
            <div className='travel-services-header'></div>
            <div className='travel-services-body'>
                <Table striped className='travel-services-table'>
                    <thead>
                        <tr>
                            {serviceColumns.map((service, key) => (
                                <th key={`${key}-service-head`}>
                                    <Header
                                        type='fS18 tertiary fW500'
                                        className='travel-service-empty-row'>
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
                                    <Header type='fW600 fS28 primary'>
                                        {userRole == ADMIN
                                            ? "You have added no services."
                                            : "There are no services."}
                                    </Header>
                                </td>
                            </tr>
                        ) : (
                            travelServices.map((service, key) => (
                                <tr key={`${key}-tr-service`}>
                                    {serviceColumns.map((item, cellKey) => (
                                        <td
                                            className='travel-services-cell'
                                            key={`${key}-ts-cell`}>
                                            <Header type='fW400 fS18 tertiary'>
                                                {getServiceCell(item, service)}
                                            </Header>
                                        </td>
                                    ))}
                                </tr>
                            ))
                        )}
                    </tbody>
                </Table>
            </div>
        </div>
    );
};

export default TravelServices;
