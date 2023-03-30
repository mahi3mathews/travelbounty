import DateTimePicker from "react-datetime-picker";
import "./datepicker.scss";
import Header from "../header/Header";

const DatePicker = ({
    value,
    minDate,
    placeholderText,
    className,
    handleChange,
    error,
}) => {
    return (
        <div className='datepicker-container'>
            <DateTimePicker
                minDate={minDate}
                value={value}
                placeholderText={placeholderText}
                className={`${className} datepicker`}
                onChange={handleChange}
            />
            {error && (
                <Header type='error fW500 fS17' className='datepicker-error'>
                    {error}
                </Header>
            )}
        </div>
    );
};

export default DatePicker;
