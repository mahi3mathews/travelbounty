import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
    fetchAgentBookingSalesTimeAsync,
    fetchAllBookingSalesTimeAsync,
} from "../../api/salesApi";
import { ADMIN, AGENT } from "../../constants/user_roles";
import Dropdown from "../../components/dropdown/Dropdown";
import Header from "../../components/header/Header";
import chroma from "chroma-js";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import { capitalize } from "@mui/material";
import { updateBookingSales } from "../../redux/sales/salesReducer";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
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

const BookingSalesChart = ({}) => {
    const dispatch = useDispatch();
    const [userId, userRole, bookingSales] = useSelector((states) => [
        states?.users?.userDetails?.userId,
        states?.users?.userDetails?.role,
        states?.sales?.bookingSales ?? [],
    ]);
    const [filter, setFilter] = useState("daily");
    const [isLoading, setLoading] = useState(false);

    const setupBookingSales = async (filterKey) => {
        let res;
        if (userRole === ADMIN) {
            res = await fetchAllBookingSalesTimeAsync(userId, filterKey);
        } else if (userRole === AGENT) {
            res = await fetchAgentBookingSalesTimeAsync(userId, filterKey);
        }
        dispatch(updateBookingSales(res?.length > 0 ? res : []));
        setLoading(false);
    };
    useEffect(() => {
        if (userId && userRole) {
            setLoading(true);
            setupBookingSales(filter);
        }
    }, [userId, userRole, filter]);

    const labels = bookingSales.map((item) => Object.keys(item)[0]);
    const colors = chroma
        .scale(["#3a3335", "#0c8346"])
        .mode("lch")
        .colors(bookingSales?.length);

    const data = {
        labels,
        datasets: [
            {
                label: "All bookings",
                backgroundColor: chroma(colors[colors?.length - 1])
                    .alpha(0.5)
                    .css(),
                data: bookingSales.map((sale, index) => {
                    console.log(sale, "SALE", Object.values(sale)[0]);
                    return Object.values(sale)[0];
                }),
            },
        ],
    };
    return (
        <div className='booking-sales-chart'>
            <div className='booking-sales-chart-header'>
                <Header type='fS21 fW500 primary'>
                    Booking sales {filter}
                </Header>
                <Dropdown
                    variant='secondary'
                    filler='primary'
                    value={capitalize(filter)}
                    handleChange={(data) => setFilter(data?.value)}
                    menu={[
                        { title: "Daily", data: { value: "daily" } },
                        { title: "Weekly", data: { value: "weekly" } },
                        { title: "Monthly", data: { value: "monthly" } },
                    ]}
                />
            </div>
            <div className='booking-sales-chart-content'>
                <Bar options={options} data={data} />
            </div>
        </div>
    );
};

export default BookingSalesChart;
