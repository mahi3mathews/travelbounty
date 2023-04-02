import { useDispatch, useSelector } from "react-redux";
import { fetchUserServiceSalesAsync } from "../../api/salesApi";
import { useEffect } from "react";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Filler,
    Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import chroma from "chroma-js";
import Header from "../../components/header/Header";
import { updateServiceSales } from "../../redux/sales/salesReducer";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Filler,
    Legend
);
const options = {
    responsive: true,
    plugins: {
        legend: {
            position: "top",
        },
    },
};

const ServiceSales = ({ travelServices = [] }) => {
    const dispatch = useDispatch();
    const [userId, serviceSales] = useSelector((states) => [
        states?.users?.userDetails?.userId,
        states?.sales?.serviceSales ?? {},
    ]);
    const setupServiceSales = async () => {
        let res = await fetchUserServiceSalesAsync(userId);
        dispatch(updateServiceSales(res));
    };
    useEffect(() => {
        if (userId) setupServiceSales();
    }, [userId]);

    const colors = chroma
        .scale(["#3a3335", "#0c8346"])
        .mode("lch")
        .colors(travelServices.length);

    const data = {
        labels: travelServices.map((service) => service?.name),
        datasets: [
            {
                fill: true,
                label: "All Services",
                data: travelServices.map(
                    (service) => serviceSales[service?.id]
                ),
                borderColor: colors[colors?.length - 1],
                backgroundColor: chroma(colors[colors?.length - 1])
                    .alpha(0.5)
                    .css(),
            },
        ],
    };

    return (
        <div className='service-sales'>
            <div className='agent-service-sales-header'>
                <Header type='fS21 fW500 primary'>Service Sales</Header>
            </div>
            <div className='agent-service-sales-content'>
                <Line options={options} data={data} />
            </div>
        </div>
    );
};

export default ServiceSales;
