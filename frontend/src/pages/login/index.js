import Card from "../../components/card/Card";
import Header from "../../components/header/Header";
import "./login.scss";
import { TextField } from "@mui/material";
import { Form, Formik, useFormik, ErrorMessage } from "formik";
import * as Yup from "yup";
import Button from "../../components/button/Button";
import Input from "../../components/input/Input";
import { REGISTER_URL, HOME_URL } from "../../constants/route_urls";
import { useNavigate } from "react-router-dom";
import { loginAsync } from "../../api/usersApi";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { setUserDetails } from "../../redux/users/userReducer";

const LoginSchema = Yup.object().shape({
    email: Yup.string().email("Invalid email").required("Required"),
    password: Yup.string().required("Required"),
});

const Login = () => {
    const [mainError, setError] = useState("");
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const handleLoginUser = async (data) => {
        let res = await loginAsync(data);
        if (res.status) {
            setError(res.message);
        } else if (res?.user_id) {
            console.log(res?.user_id);
            res.userId = res?.user_id;
            delete res.user_id;
            localStorage.setItem("isUserLoggedIn", true);
            localStorage.setItem("userId", res?.userId);
            dispatch(setUserDetails(res));
            navigate(HOME_URL);
        }
    };
    const handleRegister = () => navigate(REGISTER_URL);
    const formik = useFormik({
        initialValues: {
            email: "",
            password: "",
        },
        onSubmit: handleLoginUser,
        validationSchema: LoginSchema,
    });

    const { errors, touched } = formik;

    return (
        <div className='login'>
            <Card className='login-card'>
                <div className='login-header'>
                    <Header
                        type='secondary fW500 fS28'
                        className='login-header'>
                        Travel Bounty
                    </Header>
                </div>
                <div className='login-form'>
                    <Formik>
                        <form
                            onSubmit={formik.handleSubmit}
                            className='login-form-container'>
                            <Input
                                required
                                id='email'
                                variant='secondary'
                                className='login-form-field'
                                value={formik.values.email}
                                placeholder='Email'
                                type='text'
                                handleChange={formik.handleChange}
                                handleBlur={formik.handleBlur}
                                error={
                                    errors.email && touched.email
                                        ? errors.email
                                        : ""
                                }
                            />
                            <Input
                                required
                                id='password'
                                variant='secondary'
                                className='login-form-field'
                                value={formik.values.password}
                                placeholder='Password'
                                type='password'
                                handleChange={formik.handleChange}
                                handleBlur={formik.handleBlur}
                                error={
                                    errors.password && touched.password
                                        ? errors.password
                                        : ""
                                }
                            />

                            <div className='login-form-field login-submit'>
                                <Button
                                    type='submit'
                                    variant='primary'
                                    fontType='fW600 fS18 secondary'
                                    className='login-submit-btn'
                                    error={mainError}>
                                    Login
                                </Button>
                            </div>
                            <div className='login-form-field login-register-link'>
                                <Header type='primary fW500 fS18'>
                                    Don't have an account?
                                </Header>
                                <Button
                                    onClick={handleRegister}
                                    variant='transparent'
                                    fontType='fW600 fS18 primary'
                                    className='login-submit-btn'>
                                    Register here.
                                </Button>
                            </div>
                        </form>
                    </Formik>
                </div>
            </Card>
        </div>
    );
};

export default Login;
