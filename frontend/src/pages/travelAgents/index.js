import { useEffect, useState } from "react";
import { Spinner, Table } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { fetchAgentsAsync } from "../../api/usersApi";
import Header from "../../components/header/Header";
import { setAgentUsers } from "../../redux/users/userReducer";
import "./travelAgents.scss";

const TravelAgents = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [isLoading, setLoading] = useState(false);
    const [agentList, userId] = useSelector((states) => [
        states?.users?.agents,
        states?.users?.userDetails?.userId,
    ]);
    const agentColumns = ["Name", "Email", "Booking count", "Itinerary count"];
    const fetchAgentList = async () => {
        let res = await fetchAgentsAsync(userId);
        setTimeout(() => setLoading(false), 1500);
        dispatch(setAgentUsers(res));
    };
    const handleRowClick = (agent) => {
        navigate(agent?.user_id);
    };
    const getAgentCell = (column, agentInfo) => {
        switch (column) {
            case "Name":
                return agentInfo?.name ?? "-";
            case "Email":
                return agentInfo?.email ?? "-";
            case "Booking count":
                return agentInfo?.booking_count ?? "-";
            case "Itinerary count":
                return agentInfo?.booking_count ?? "-";
            default:
                return "-";
        }
    };
    useEffect(() => {
        if (userId) {
            setLoading(true);
            fetchAgentList();
        }
    }, [userId]);
    return (
        <div className='travel-agents-container'>
            <div className='travel-agents-header'>
                <Header type='fW600 fS32 tertiary'>Travel Agents</Header>
            </div>
            <div className='travel-agents-body'>
                {isLoading ? (
                    <Spinner />
                ) : (
                    <Table striped bordered className='travel-agents-table'>
                        <thead>
                            <tr>
                                {agentColumns.map((service, key) => (
                                    <th
                                        key={`${key}-service-head`}
                                        className='travel-agents-column-head'>
                                        <Header
                                            type='fS21 tertiary fW600'
                                            className='travel-agents-column'>
                                            {service}
                                        </Header>
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {agentList.length <= 0 ? (
                                <tr>
                                    <td colSpan={4}>
                                        <Header
                                            type='fW600 fS28 primary'
                                            className='travel-agents-empty-row'>
                                            No agents have signed up yet.
                                        </Header>
                                    </td>
                                </tr>
                            ) : (
                                agentList.map((agent, key) => (
                                    <tr
                                        onClick={() => handleRowClick(agent)}
                                        key={`${key}-tr-service`}
                                        className='travel-agents-row'>
                                        {agentColumns.map((item, cellKey) => (
                                            <td
                                                className='travel-agents-cell'
                                                key={`${key}${cellKey}-ts-cell`}>
                                                <Header type='fW400 fS18 tertiary'>
                                                    {getAgentCell(item, agent)}
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

export default TravelAgents;
