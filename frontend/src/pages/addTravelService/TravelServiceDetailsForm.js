import { Form } from "react-bootstrap";
import DateTimePicker from "react-datetime-picker";
import DatePicker from "../../components/datepicker/Datepicker";
import Header from "../../components/header/Header";
import Input from "../../components/input/Input";
import {
    accommodationDetails,
    activityDetails,
    transportationDetails,
    flightDetails,
} from "../../constants/travelServiceTypes";

const TravelServiceDetailsForm = ({
    type,
    formValues,
    formErrors,
    formTouched,
    handleFormUpdate,
}) => {
    const typeDetails = (type) => {
        switch (type) {
            case "TRANSPORTATION":
                return transportationDetails;
            case "ACTIVITY":
                return activityDetails;
            case "FLIGHT":
                return flightDetails;
            case "ACCOMMODATION":
                return accommodationDetails;
            default:
                return [];
        }
    };

    let details = typeDetails(type);

    const getFormField = (fieldData) => {
        switch (fieldData.fieldType) {
            case "text":
                return (
                    <Input
                        required
                        type='text'
                        value={formValues?.[fieldData?.key] ?? ""}
                        placeholder={fieldData?.placeholder}
                        id={fieldData?.key}
                        className='add-travel-service-details-input'
                        handleChange={(e) =>
                            handleFormUpdate(fieldData?.key, e?.target?.value)
                        }
                        error={
                            formErrors?.[fieldData?.key] &&
                            formTouched?.[fieldData?.key]
                                ? formErrors?.[fieldData?.key]
                                : ""
                        }
                    />
                );
            case "datepicker":
                return (
                    <DatePicker
                        minDate={new Date()}
                        value={formValues?.[fieldData?.key] ?? ""}
                        placeholderText={fieldData?.placeholder}
                        className='add-travel-service-details-date'
                        handleChange={(value) =>
                            handleFormUpdate(fieldData?.key, value)
                        }
                        error={
                            formErrors?.[fieldData?.key] &&
                            formTouched?.[fieldData?.key]
                                ? formErrors?.[fieldData?.key]
                                : ""
                        }
                    />
                );
        }
    };

    return (
        <div className='travel-details-form'>
            {details.map((item, key) => (
                <Form.Group
                    key={`${key}-form-field`}
                    className='add-travel-service-form-group'>
                    <Form.Label>
                        <Header type='fS21 fW500 tertiary'>
                            {item?.placeholder}{" "}
                        </Header>
                    </Form.Label>
                    {getFormField(item)}
                </Form.Group>
            ))}
        </div>
    );
};

export default TravelServiceDetailsForm;
