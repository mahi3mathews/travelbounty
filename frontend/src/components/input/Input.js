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
    preChar,
    name = "",
    maxLength,
}) => {
    const handleKeyDown = (e) => {
        if (type === "text-number") {
            if (
                [46, 8, 9, 27, 13, 110, 190].includes(e.keyCode) ||
                (e.keyCode === 65 && e.ctrlKey === true) ||
                (e.keyCode === 67 && e.ctrlKey === true) ||
                (e.keyCode === 86 && e.ctrlKey === true) ||
                (e.keyCode === 88 && e.ctrlKey === true)
            ) {
                return;
            }
            if (
                (e.keyCode < 48 || e.keyCode > 57) &&
                (e.keyCode < 96 || e.keyCode > 105)
            ) {
                e.preventDefault();
            }
        }
    };
    const handleInputChange = (e) => {
        let newValue = e.target.value;
        if (preChar) {
            newValue =
                newValue?.length > preChar?.length || newValue.includes(preChar)
                    ? String(newValue).substring(String(preChar).length)
                    : newValue;
            if (type === "text-number") newValue = Number(newValue);
            handleChange({ ...e, target: { ...e.target, value: newValue } });
        } else handleChange(e);
    };
    return (
        <div className='input'>
            <div className={`input-container ${error ? "error" : variant}`}>
                <Form.Control
                    name={name}
                    id={id}
                    required={required}
                    className={`input-field ${className ?? ""}`}
                    placeholder={placeholder ?? ""}
                    value={`${value ? preChar ?? "" : ""}${value}`}
                    onChange={handleInputChange}
                    type={type ?? "text"}
                    onBlur={handleBlur}
                    onKeyDown={handleKeyDown}
                    maxLength={maxLength}
                />
                {postComponent ?? null}
            </div>
            {error && (
                <div className='input-field-error'>
                    <Header
                        type='fW700 fS17 error'
                        className='input-field-error-txt'>
                        {error}
                    </Header>
                </div>
            )}
        </div>
    );
};

export default Input;
