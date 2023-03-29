import "./header.scss";

const Header = ({ className, type, children }) => {
    return (
        <div
            className={`header ${className ?? ""} ${
                type ?? "tertiary fW400 fS14"
            }`}>
            {children}
        </div>
    );
};

export default Header;
