import Header from "../header/Header";
import "./button.scss";
import Icon from "../icon/Icon";
import { ERROR_HEADER_TYPE } from "../../constants/header_types";

const Button = ({
    type,
    fontType,
    variant,
    onClick,
    className,
    children,
    error,
    preIcon,
}) => {
    return (
        <div className='bttn-container'>
            <button
                type={type}
                className={`${variant} bttn ${className}`}
                onClick={onClick}>
                {preIcon && <Icon src={preIcon} className='bttn-pre-icon' />}
                <Header type={fontType ?? "fW600 tertiary fS18"}>
                    {children}
                </Header>
            </button>

            {error && (
                <Header type={ERROR_HEADER_TYPE} className='bttn-error'>
                    {error}
                </Header>
            )}
        </div>
    );
};

export default Button;
