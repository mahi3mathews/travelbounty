import { Card as ReactCard } from "react-bootstrap";
import "./card.scss";

// Custom Card component with common style for entire application
const Card = ({ children, index, className, onClick = () => {} }) => {
    return (
        <ReactCard
            key={`${index}-${className}`}
            onClick={onClick}
            className={`${className ?? ""} card`}>
            {children}
        </ReactCard>
    );
};

export default Card;
