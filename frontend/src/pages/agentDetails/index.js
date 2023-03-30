import "./agentDetails.scss";
import Header from "../../components/header/Header";
import Card from "../../components/card/Card";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { fetchAgentDetailsAsync } from "../../api/usersApi";
import RoundedIcon from "../../components/roundedIcon/RoundedIcon";
import add from "../../icons/add-secondary.svg";
import Button from "../../components/button/Button";
import { monthNames } from "../../constants/dates";
import Modal from "../../components/modal/Modal";
import Input from "../../components/input/Input";
import { addAgentIncentiveAsync } from "../../api/paymentsApi";

const AgentDetails = () => {
    const [userId] = useSelector((states) => [
        states?.users?.userDetails?.userId,
    ]);
    const { id } = useParams();

    const [agentDetails, setAgentDetails] = useState({});
    const [showModal, setShowModal] = useState(false);
    const [incentiveAmount, setIncentiveAmount] = useState("");
    const [incentiveError, setIncentiveErr] = useState("");

    const handleHideModal = () => setShowModal(false);

    const getNameInitials = (name) => {
        if (name) {
            let nameArr = name.split(" ");
            return `${nameArr[0][0]}${nameArr[nameArr.length - 1][0]}`;
        }
    };

    const handleAddIncentive = () => setShowModal(true);
    const handleSubmit = async () => {
        if (incentiveAmount < 0) {
            setIncentiveErr("Amount should be greater than 0.");
        } else {
            let res = await addAgentIncentiveAsync(
                { amount: incentiveAmount },
                id,
                userId
            );
            if (res.includes("Success")) {
                handleHideModal();
            } else {
                // handle button error
            }
        }
    };

    const fetchAgentInfo = async () => {
        let res = await fetchAgentDetailsAsync(id);
        setAgentDetails(res);
    };
    const renderRow = (label, value, key) => {
        return (
            <div key={`${key}-label-row`} className='agent-details-content-row'>
                <Header
                    type='fW500 fS21 secondary'
                    className='agent-details-content-label'>
                    {label}
                </Header>
                <Header
                    type='fW600 fS24 secondary'
                    className='agent-details-content-label'>
                    {value}
                </Header>
            </div>
        );
    };
    const rowDetails = [
        {
            label: "Bookings",
            value: `#${agentDetails?.booking_count}`,
        },
        {
            label: "Itineraries count",
            value: `#${agentDetails?.itinerary_count}`,
        },
        {
            label: "Total booking sale",
            value: `£ ${agentDetails?.total_bookings_sale}`,
        },
        {
            label: `${monthNames[new Date().getMonth()]} booking sale`,
            value: `£ ${agentDetails?.month_bookings_sale ?? 0}`,
        },
        {
            label: `${monthNames[new Date().getMonth()]} commission earned`,
            value: `£ ${agentDetails?.total_monthly_commission ?? 0}`,
        },
    ];
    useEffect(() => {
        if (id) {
            fetchAgentInfo();
        }
    }, [id]);
    return (
        <div className='agent-details'>
            <Modal
                className='agent-details-modal'
                show={showModal}
                onHide={handleHideModal}
                onSubmit={handleSubmit}
                title='Agent Incentive'
                footerBtn='Submit'>
                <div className='agent-details-modal-content'>
                    <Header
                        type='fW500 fS21 tertiary'
                        className='agent-details-content-label'>
                        Incentive
                    </Header>
                    <Input
                        required
                        type='text-number'
                        placeholder='Incentive amount'
                        id='price'
                        className='add-travel-service-price'
                        preChar='£ '
                        value={incentiveAmount}
                        handleChange={(e) => setIncentiveAmount(e.target.value)}
                        error={incentiveError}
                    />
                </div>
            </Modal>
            <Card className='agent-details-header'>
                <RoundedIcon
                    fontType='fW700 fS32 primary'
                    variant='secondary'
                    text={getNameInitials(agentDetails?.name)}
                />
                <Header
                    type='fW700 fS28 secondary'
                    className='agent-details-title'>
                    {`${agentDetails?.name} `}
                </Header>
                <Header
                    type='fW600 fS24 secondary'
                    className='agent-details-title-id'>
                    {` - #${agentDetails?.user_id}`}
                </Header>
            </Card>
            <div className='agent-details-body'>
                <Card className='agent-details-content'>
                    <div className='agent-details-content-header'>
                        <Header
                            type='fW500 fS32 primary'
                            className='agent-details-content-title'>
                            Agent sales info
                        </Header>
                        <Button
                            variant='primary'
                            fontType='fS18 fW600 secondary'
                            preIcon={add}
                            onClick={handleAddIncentive}
                            className='agent-detials-content-add-incentive'>
                            Add incentive
                        </Button>
                    </div>
                    {rowDetails.map((item, key) =>
                        renderRow(item?.label, item?.value, key)
                    )}
                </Card>
            </div>
        </div>
    );
};

export default AgentDetails;
