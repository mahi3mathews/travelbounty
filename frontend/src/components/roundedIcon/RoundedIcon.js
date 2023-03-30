import "./roundedIcon.scss";
import Header from "../header/Header";

const RoundedIcon = ({ variant, fontType, text, className = "" }) => {
    return (
        <div className={`${className} rounded-icon ${variant ?? "tertiary"}`}>
            {<Header type={fontType}>{text}</Header>}
        </div>
    );
};

export default RoundedIcon;
