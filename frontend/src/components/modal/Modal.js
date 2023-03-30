import Header from "../header/Header";
import Button from "../button/Button";
import { Modal as ReactModal } from "react-bootstrap";
import "./modal.scss";

const Modal = ({
    show,
    title = "",
    footerBtn,
    children = "",
    submitError = "",
    onSubmit = () => {},
    onHide = () => {},
}) => {
    return (
        <ReactModal
            className='custom-modal'
            show={show}
            onHide={onHide}
            size='lg'
            aria-labelledby='contained-modal-title-vcenter'
            centered>
            {title && (
                <ReactModal.Header closeButton className='custom-modal-header'>
                    <ReactModal.Title id='contained-modal-title-vcenter'>
                        <Header
                            type='fW700 fS21 tertiary'
                            className='custom-modal-header-title'>
                            {title}
                        </Header>
                    </ReactModal.Title>
                </ReactModal.Header>
            )}
            <ReactModal.Body className='custom-modal-body'>
                {children}
            </ReactModal.Body>
            {footerBtn && (
                <ReactModal.Footer>
                    <Button
                        variant='primary'
                        fontType='fW600 fS18 secondary'
                        onClick={onSubmit}
                        error={submitError}>
                        {footerBtn}
                    </Button>
                </ReactModal.Footer>
            )}
        </ReactModal>
    );
};

export default Modal;
