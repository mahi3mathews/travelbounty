import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getUserDetailsAsync } from "./api/usersApi";
import "./App.scss";
import Sidebar from "./components/sidebar/Sidebar";
import { updateUserDetails } from "./redux/users/userReducer";
import AppRouter from "./router/appRouter";

function App() {
    const dispatch = useDispatch();

    const [isLoggedIn, setLoggedIn] = useState(false);
    const [userId, userRole] = useSelector((states) => [
        states?.users?.userDetails?.userId ?? "",
        states?.users?.userDetails?.role ?? "",
    ]);

    const setUserDetails = async () => {
        let userRes = await getUserDetailsAsync(localStorage.getItem("userId"));
        if (userRes?.user_id) {
            userRes.userId = userRes?.user_id;
            delete userRes?.user_id;
            dispatch(updateUserDetails(userRes));
        }
    };

    useEffect(() => {
        // Set up check to see if user is still logged in.

        const isLoggedIn = localStorage.getItem("isUserLoggedIn") === "true";
        setLoggedIn(isLoggedIn);
        if (isLoggedIn && !userId) {
            setUserDetails();
        }
    }, [userId]);

    return (
        <div className='app'>
            {isLoggedIn && <Sidebar />}
            <div className='app-body'>
                <AppRouter />
            </div>
        </div>
    );
}

export default App;
