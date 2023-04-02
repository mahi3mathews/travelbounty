import { capitalize } from "@mui/material";
import { Form } from "react-bootstrap";
import Card from "../../components/card/Card";
import Header from "../../components/header/Header";
import "./serviceCheckList.scss";

const ServiceCheckList = ({
    services = [],
    handleCheckClick,
    className,
    checkedList,
    checkDisabled = false,
    allChecked = false,
    singleSelect = false,
}) => {
    return (
        <div className={`${className} service-check-list`}>
            <Card className='service-check-list-card'>
                {services.map((service, key) => {
                    return (
                        <div
                            className='service-check-list-item'
                            key={`${key}-sevice-check`}>
                            <Form.Check
                                disabled={checkDisabled}
                                onChange={(e) => handleCheckClick(service)}
                                className={`service-check-list-checkbox`}
                                checked={
                                    checkedList?.includes(service?.id) ||
                                    allChecked
                                }
                                label={
                                    <div className='service-check-list-label'>
                                        <Header type='fS21 fW600 primary'>
                                            {service?.name}
                                        </Header>
                                        <Header type='fS18 fW500 primary'>
                                            {capitalize(
                                                (
                                                    service?.type ??
                                                    service?.description ??
                                                    ""
                                                ).toLowerCase()
                                            )}
                                        </Header>
                                    </div>
                                }
                            />
                            <Header
                                type='fS21 fW600 primary'
                                className='service-check-list-price'>
                                {`£ ${service?.price ?? service?.total_price}`}
                            </Header>
                        </div>
                    );
                })}
            </Card>
        </div>
    );
};

export default ServiceCheckList;
