import { Form } from "react-bootstrap";
import "./input.scss";
import Header from "../header/Header";

// Custom input component with common style for entire application
const Input = ({
    placeholder,
    className,
    value,
    postComponent,
    handleChange = () => {},
    handleBlur = () => {},
    type,
    id,
    required,
    variant,
    error,
}) => {
    return (
        <div className='input-error-container'>
            <div className={`input-container ${error ? "error" : variant}`}>
                <Form.Control
                    id={id}
                    required={required}
                    className={`input-field ${className ?? ""}`}
                    placeholder={placeholder ?? ""}
                    value={value}
                    onChange={handleChange}
                    type={type ?? "text"}
                    onBlur={handleBlur}
                />
                {postComponent ?? null}
            </div>
            {error && (
                <div className='input-field-error'>
                    <Header
                        type='fW600 fS16 error'
                        className='input-field-error-txt'>
                        {error}
                    </Header>
                </div>
            )}
        </div>
    );
};

export default Input;
