import "./agentDetails.scss";

import { useParams } from "react-router-dom";
import { useEffect } from "react";
import { useSelector } from "react-redux";
import { fetchAgentDetailsAsync } from "../../api/usersApi";

const AgentDetails = () => {
    const [userId] = useSelector((states) => [
        states?.users?.userDetails?.userId,
    ]);
    const { id } = useParams();

    const fetchAgentInfo = async () => {
        let res = await fetchAgentDetailsAsync(id);
        console.log(res);
    };
    useEffect(() => {
        console.log("users");
        if (id) {
            fetchAgentInfo();
        }
    }, [id]);
    return <div className='agent-details'></div>;
};

export default AgentDetails;
