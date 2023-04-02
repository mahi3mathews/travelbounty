import { useDispatch, useSelector } from "react-redux";
import { fetchAgentSalesCommissionAsync } from "../../api/salesApi";
import { useEffect } from "react";
import { AGENT } from "../../constants/user_roles";
import { updateServiceComissions } from "../../redux/sales/salesReducer";
import { Doughnut } from "react-chartjs-2";
import chroma from "chroma-js";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import Header from "../../components/header/Header";
import { useRef } from "react";

ChartJS.register(ArcElement, Tooltip, Legend);

const ServiceCommissions = ({ travelServices = [] }) => {
    const dispatch = useDispatch();

    const [userId, userRole, serviceCommissions] = useSelector((states) => [
        states?.users?.userDetails?.userId,
        states?.users?.userDetails?.role,
        states?.sales?.serviceCommissions ?? {},
    ]);
    const setupServiceCommissions = async () => {
        let res = await fetchAgentSalesCommissionAsync(userId);
        if (Object.keys(res)?.length > 0) {
            dispatch(updateServiceComissions(res));
        }
    };
    useEffect(() => {
        if (userId && userRole === AGENT) setupServiceCommissions();
    }, [userId, userRole]);

    const colors = chroma
        .scale(["#3a3335", "#0c8346"])
        .mode("lch")
        .colors(travelServices.length);

    const data = {
        labels: travelServices.map((item) => item?.name),
        datasets: [
            {
                label: "£ commission earned",
                data: travelServices.map(
                    (item) => serviceCommissions[item?.id]
                ),
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 1,
            },
        ],
    };

    return (
        <div className='service-commissions'>
            {userRole === AGENT && (
                <>
                    <div className='service-commissions-header'>
                        <Header type='fS21 fW500 primary'>
                            Service Commissions
                        </Header>
                    </div>
                    <div className='service-commissions-content'>
                        {Object.keys(serviceCommissions)?.length <= 0 ? (
                            <Header
                                type='fS21 fW500 tertiary'
                                className='service-commissions-content-empty'>
                                You have no commissions yet.
                            </Header>
                        ) : (
                            <Doughnut
                                data={data}
                                className='service-commissions-graph'
                            />
                        )}
                    </div>
                </>
            )}
        </div>
    );
};

export default ServiceCommissions;
