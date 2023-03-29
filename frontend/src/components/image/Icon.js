import Image from "react-bootstrap/Image";

const Icon = ({ src, icon, className }) => {
    if (icon) return <Image src={icon} className={`img ${className}`} />;
    return <img src={src} className={`img ${className}`} />;
};

export default Icon;
