import Card from "../../components/card/Card";
import Header from "../../components/header/Header";
import "./register.scss";
import { Formik, useFormik } from "formik";
import * as Yup from "yup";
import Button from "../../components/button/Button";
import Input from "../../components/input/Input";
import { LOGIN_URL } from "../../constants/route_urls";
import Switch from "react-switch";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { registerUserAsync } from "../../api/usersApi";

const RegisterSchema = Yup.object().shape({
    email: Yup.string().email("Invalid email").required("Required"),
    password: Yup.string().required("Required"),
});

const Register = () => {
    const [isLoading, setLoading] = useState(false);
    const [isAdminRole, setAdminRole] = useState(false);
    const [mainError, setError] = useState("");
    const navigate = useNavigate();
    const handleRegisterUser = async (data) => {
        setError("");
        let res = await registerUserAsync({ ...data, isAdmin: isAdminRole });

        setTimeout(() => {
            if (res.status) {
                setLoading(false);
                setError(res.message);
            } else {
                navigate(LOGIN_URL);
            }
        }, 1000);
    };
    const handleLogin = () => navigate(LOGIN_URL);
    const formik = useFormik({
        initialValues: {
            name: "",
            email: "",
            password: "",
        },
        onSubmit: handleRegisterUser,
        validationSchema: RegisterSchema,
    });

    const { errors, touched } = formik;
    return (
        <div className='register'>
            <Card className='register-card'>
                <div className='register-header'>
                    <Header
                        type='secondary fW600 fS24'
                        className='register-header'>
                        Register
                    </Header>
                </div>
                <div className='register-form'>
                    <Formik>
                        <form
                            onSubmit={formik.handleSubmit}
                            className='register-form-container'>
                            <Input
                                id='name'
                                required
                                className='register-form-field'
                                value={formik.values.name}
                                placeholder='Name'
                                type='text'
                                handleChange={formik.handleChange}
                                handleBlur={formik.handleBlur}
                                error={
                                    errors.name && touched.name
                                        ? errors.name
                                        : ""
                                }
                            />
                            <Input
                                id='email'
                                required
                                className='register-form-field'
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
                                id='password'
                                required
                                className='register-form-field'
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
                            <div className='register-form-switch'>
                                <Switch
                                    id='isAdmin'
                                    className={`register-toggle ${
                                        isAdminRole ? "checked" : ""
                                    }`}
                                    onChange={(e) => setAdminRole(e)}
                                    checked={isAdminRole}
                                    onColor='#f8f2dc'
                                    offColor='#3a3335'
                                    onHandleColor='#3a3335'
                                    offHandleColor='#f8f2dc'
                                />
                                <Header
                                    type='secondary fW500 fS21'
                                    className='reigster-toggle-title'>
                                    Are you an admin?
                                </Header>
                            </div>

                            <div className='register-form-field register-submit'>
                                <Button
                                    type='submit'
                                    variant='secondary'
                                    fontType='fW600 fS18 tertiary'
                                    className='register-submit-bttn'
                                    error={mainError}>
                                    Create account
                                </Button>
                            </div>
                            <div className='register-form-field register-login-link'>
                                <Header type='tertiary fW500 fS18'>
                                    Have an account?
                                </Header>
                                <Button
                                    onClick={handleLogin}
                                    variant='transparent'
                                    fontType='fW600 fS18 tertiary'
                                    className='register-submit-bttn'>
                                    Login here.
                                </Button>
                            </div>
                        </form>
                    </Formik>
                </div>
            </Card>
        </div>
    );
};
export default Register;
