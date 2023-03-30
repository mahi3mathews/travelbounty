import Image from "react-bootstrap/Image";
import "./icon.scss";

const Icon = ({ src, icon, className, onClick }) => {
    if (icon) return <Image src={icon} className={`img ${className}`} />;
    return (
        <img
            src={src}
            className={`icon ${className} ${onClick ? "cursor" : ""}`}
            onClick={onClick ?? (() => {})}
        />
    );
};

export default Icon;
