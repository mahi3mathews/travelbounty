import { useDispatch } from "react-redux";
import { resetSales } from "../../redux/sales/salesReducer";
import { resetTravelService } from "../../redux/travelServices/travelServiceReducer";
import { resetUser } from "../../redux/users/userReducer";
// Logout component to handle state removal of user.

const Logout = () => {
    const dispatch = useDispatch();
    localStorage.removeItem("isUserLoggedIn");
    localStorage.removeItem("userId");
    dispatch(resetUser());
    dispatch(resetSales());
    dispatch(resetTravelService());
    return <></>;
};

export default Logout;
