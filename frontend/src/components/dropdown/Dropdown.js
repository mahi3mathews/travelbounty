import { Dropdown as ReactDropdown } from "react-bootstrap";
import Header from "../header/Header";
import "./dropdown.scss";
import { useEffect, useRef, useState } from "react";
import Icon from "../image/Icon";

// Custom dropdown component with common style for entire application
const Dropdown = ({
    className = "",
    handleChange,
    value,
    menu = [],
    error,
}) => {
    const [showMenu, setShowMenu] = useState(false);
    const [title, setTitle] = useState(value);

    const wrapperRef = useRef(null);

    const handleOutsideClick = (event) => {
        if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
            setShowMenu(false);
        }
    };

    useEffect(() => {
        document.addEventListener("mousedown", handleOutsideClick);
        return () => {
            document.removeEventListener("mousedown", handleOutsideClick);
        };
    }, []);

    useEffect(() => {
        setTitle(value);
    }, [value]);

    const handleItemClick = (item) => {
        handleChange(item.data);
        setTitle(item.title);
        setShowMenu(false);
    };

    return (
        <div className='custom-dropdown-container'>
            <ReactDropdown
                ref={wrapperRef}
                className={`custom-dropdown ${className}`}>
                <ReactDropdown.Toggle
                    id='dropdown-autoclose-true'
                    className={`custom-dropdown-toggle ${error ? "error" : ""}`}
                    variant='transparent'
                    onClick={() => {
                        setShowMenu((prevState) => !prevState);
                    }}>
                    <Header
                        className='custom-dropdown-toggle-text'
                        type={`fS16 fW400 ${error ? "error" : "tertiary"}`}>
                        {title}
                    </Header>
                    <Icon />
                </ReactDropdown.Toggle>
                <div className='menu-container'>
                    <div className={`menu ${showMenu ? "show" : "hide"}`}>
                        {menu.map((item, index) => (
                            <div
                                className='menu-item'
                                key={`${index}-drop-item`}
                                onClick={() => handleItemClick(item)}>
                                <Header type='fW600 fS16 secondary'>
                                    {item.title}
                                </Header>
                            </div>
                        ))}
                    </div>
                </div>
            </ReactDropdown>
            {error && (
                <div className='custom-dropdown-error'>
                    <Header
                        type='error fW700 fS17'
                        className='custom-dropdown-error-content'>
                        {error}
                    </Header>
                </div>
            )}
        </div>
    );
};

export default Dropdown;
