import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { travelAgentServiceSalesAsync } from "../../api/salesApi";
import { fetchTravelServicesAsync } from "../../api/travelServiceApi";
import { updateAgentServiceSales } from "../../redux/sales/salesReducer";
import { updateServiceList } from "../../redux/travelServices/travelServiceReducer";

const TravelAgentServiceSales = () => {
    const dispatch = useDispatch();
    const [userId, serviceSales, travelServices] = useSelector((states) => [
        states?.users?.userDetails?.userId,
        states?.sales?.agentServiceSales,
        states?.travelServices?.serviceList ?? [],
    ]);

    const getServiceSales = async () => {
        let travelServiceRes = await fetchTravelServicesAsync();
        console.log(travelServiceRes);
        dispatch(updateServiceList(travelServiceRes));
        let data = await travelAgentServiceSalesAsync(userId);
        console.log(data, "DATA");
        if (data?.id) {
            dispatch(updateAgentServiceSales({ data }));
        }
    };
    useEffect(() => {
        console.log(userId, "USER ID");
        if (userId) getServiceSales();
    }, [userId]);
    return <div className='agent-service-sales'></div>;
};

export default TravelAgentServiceSales;