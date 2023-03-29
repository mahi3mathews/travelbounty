import Header from "../header/Header";
import "./button.scss";
import { Spinner } from "react-bootstrap";

const Button = ({
    type,
    fontType,
    variant,
    onClick,
    className,
    children,
    error,
}) => {
    return (
        <div className='btn-container'>
            <button
                type={type}
                className={`${variant} btn cursor ${className}`}
                onClick={onClick}>
                <Header type={fontType ?? "fW600 tertiary fS18"}>
                    {children}
                </Header>
            </button>

            {error && (
                <Header type='error fW700 fS17' className='btn-error'>
                    {error}
                </Header>
            )}
        </div>
    );
};

export default Button;
