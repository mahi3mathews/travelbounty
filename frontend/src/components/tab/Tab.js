import { Tabs, Tab as ReactTab } from "react-bootstrap";
import "./tab.scss";

const Tab = ({ defaultKey, tabs, className }) => {
    return (
        <Tabs
            defaultActiveKey={defaultKey}
            id='justify-tab'
            className={`custom-tab ${className}`}>
            {tabs.map((tab, key) => (
                <ReactTab
                    eventKey={tab?.key}
                    title={tab?.title}
                    key={`${key}-tab-item`}>
                    {tab?.content}
                </ReactTab>
            ))}
        </Tabs>
    );
};

export default Tab;
