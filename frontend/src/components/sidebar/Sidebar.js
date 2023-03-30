import "./sidebar.scss";
import logo from "../../icons/logo.svg";
import Icon from "../image/Icon";
import { navLinks } from "../../constants/navLinks";
import { NavLink } from "react-router-dom";
import Header from "../header/Header";
import { useState } from "react";
import { ADMIN } from "../../constants/user_roles";
import { HOME_URL } from "../../constants/route_urls";

const Sidebar = () => {
    const [isHover, setIsHover] = useState(false);
    const [currentUserRole, setCurrentUserRole] = useState(ADMIN);
    const handleHover = () => setTimeout(() => setIsHover(true), 130);
    const handleLeave = () => setIsHover(false);
    return (
        <div
            className='sidebar'
            id='sidebar-1'
            onMouseEnter={handleHover}
            onMouseLeave={handleLeave}>
            <div className='sidebar-logo'>
                <NavLink to={HOME_URL} className='sidebar-logo-link'>
                    <Icon icon={logo} className='sidebar-logo-img' />
                    <Header
                        type='primary fW700 fS32'
                        className={`sidebar-logo-title${
                            isHover ? " visible" : ""
                        }`}>
                        Travel Bounty
                    </Header>
                </NavLink>
            </div>
            <div className='sidebar-nav-container'>
                {navLinks.map((nav, key) => {
                    if (nav.roles.includes(currentUserRole) && !nav.isNotNav)
                        return (
                            <div
                                className='sidebar-navlink'
                                key={`${key}-sidebar-nav`}>
                                <NavLink to={nav.link}>
                                    <Icon
                                        icon={nav.img}
                                        className='sidebar-navlink-img'
                                    />
                                    <Header
                                        type='primary fW500 fS21'
                                        className={`sidebar-navlink-title${
                                            isHover ? " visible" : ""
                                        }`}>
                                        {nav.title}
                                    </Header>
                                </NavLink>
                            </div>
                        );
                })}
            </div>
        </div>
    );
};

export default Sidebar;
