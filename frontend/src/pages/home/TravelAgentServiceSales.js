import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAllAgentServiceSalesAsync } from "../../api/salesApi";
import { updateAgentServiceSales } from "../../redux/sales/salesReducer";
import { ADMIN } from "../../constants/user_roles";
import { Line } from "react-chartjs-2";
import chroma from "chroma-js";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";
import Header from "../../components/header/Header";
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);
const lineOptions = {
    responsive: true,
    interaction: {
        mode: "index",
        intersect: false,
    },
    stacked: false,
    scales: {
        y: {
            type: "linear",
            display: true,
            position: "left",
        },
    },
};

const TravelAgentServiceSales = ({ travelServices = [] }) => {
    const dispatch = useDispatch();
    const [userId, userRole, serviceSales] = useSelector((states) => [
        states?.users?.userDetails?.userId,
        states?.users?.userDetails?.role,
        states?.sales?.agentServiceSales ?? [],
    ]);

    const labels = travelServices.map((item) => item?.name);
    const getServiceSales = async () => {
        let data = await fetchAllAgentServiceSalesAsync(userId);
        if (data?.length > 0) {
            dispatch(updateAgentServiceSales(data));
        }
    };

    const colors = chroma
        .scale(["#3a3335", "#0c8346"])
        .mode("lch")
        .colors(serviceSales?.length);

    const data = {
        labels,
        datasets: serviceSales.map((item, index) => {
            let item_label = Object.keys(item)[0];
            let color = colors[index];
            return {
                label: item_label,
                data: travelServices?.map(
                    (service) => item[item_label][service?.id]
                ),
                borderColor: color,
                backgroundColor: chroma(color).alpha(0.5).css(),
                yAxisID: "y",
            };
        }),
    };

    useEffect(() => {
        if (userId && userRole === ADMIN) getServiceSales();
    }, [userId, userRole]);
    return (
        <div className='agent-service-sales'>
            {userRole === ADMIN && (
                <>
                    <div className='agent-service-sales-header'>
                        <Header type='fS21 fW500 primary'>
                            Agent Service Sales
                        </Header>
                    </div>
                    <div className='agent-service-sales-content'>
                        <Line options={lineOptions} data={data} />
                    </div>
                </>
            )}
        </div>
    );
};

export default TravelAgentServiceSales;
