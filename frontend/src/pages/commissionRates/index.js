import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
    fetchCommissionsAsync,
    updateCommissionRateAsync,
} from "../../api/commissionApi";
import Header from "../../components/header/Header";
import { PAGE_HEADER_TYPE } from "../../constants/header_types";
import { updateCommissions } from "../../redux/commissions/commissionReducer";
import Card from "../../components/card/Card";
import "./commissionRates.scss";
import { capitalize } from "@mui/material";
import edit from "../../icons/edit.svg";
import Icon from "../../components/icon/Icon";
import Input from "../../components/input/Input";
import Button from "../../components/button/Button";
import { Alert } from "react-bootstrap";

const CommissionRates = () => {
    const dispatch = useDispatch();
    const [userId, commissionRates] = useSelector((states) => [
        states?.users?.userDetails?.userId,
        states?.commissionRates?.commissions,
    ]);
    const [isEdit, setEdit] = useState({});
    const [editRates, setEditRates] = useState({});
    const [rateError, setRateError] = useState("");
    const setupCommissions = async () => {
        let res = await fetchCommissionsAsync(userId);
        dispatch(updateCommissions(res));
        res.forEach((item) =>
            setEditRates((prevState) => ({
                ...prevState,
                [item?.service_type]: item?.commission_rate,
            }))
        );
    };
    const handleEditClick = (editKey) =>
        setEdit((prevState) => ({
            ...prevState,
            [editKey]: !prevState?.[editKey] ?? false,
        }));
    const handleUpdateRates = async (serviceType) => {
        if (editRates[serviceType] > 100) {
            setRateError("Rate cannot be more than 100.");
        } else {
            let commission = commissionRates.find(
                (commission) => commission.service_type === serviceType
            );
            let res = await updateCommissionRateAsync(
                { rate: Number(editRates[serviceType]) },
                commission?.id,
                userId
            );
            if (res?.length > 0) {
                dispatch(updateCommissions(res));
                handleEditClick(serviceType);
            }
        }
    };

    useEffect(() => {
        if (userId) {
            setupCommissions();
        }
    }, [userId]);
    return (
        <div className='commission-rates'>
            <div className='commission-rates-header'>
                <Header type={PAGE_HEADER_TYPE}>Commission Rates</Header>
            </div>
            {rateError && (
                <Alert
                    variant='danger'
                    onClose={() => setRateError("")}
                    dismissible>
                    {rateError}
                </Alert>
            )}
            <div className='commission-rates-body'>
                {commissionRates.map((commission, key) => {
                    return (
                        <div
                            className='commission-rates-item'
                            key={`${key}-rate`}>
                            <Card className='commission-rates-card'>
                                <div className='commission-rates-details'>
                                    <Header
                                        type='fS18 fW600 secondary'
                                        className='commission-rates-label'>
                                        {`${capitalize(
                                            String(
                                                commission?.service_type
                                            ).toLowerCase()
                                        )}: `}
                                    </Header>
                                    {isEdit[commission?.service_type] ? (
                                        <Input
                                            required
                                            variant='secondary'
                                            type='text-number'
                                            placeholder='Commission rate'
                                            id='rate'
                                            className='commission-rates-edit-rate'
                                            value={
                                                editRates[
                                                    commission?.service_type
                                                ]
                                            }
                                            handleChange={(e) => {
                                                setRateError("");
                                                setEditRates((prevState) => ({
                                                    ...prevState,
                                                    [commission?.service_type]:
                                                        e.target.value,
                                                }));
                                            }}
                                        />
                                    ) : (
                                        <Header
                                            type='fS18 fW600 secondary'
                                            className='commission-rates-value'>
                                            {`${commission?.commission_rate}%`}
                                        </Header>
                                    )}
                                </div>
                                <div className='commission-rates-edit'>
                                    {isEdit[commission?.service_type] ? (
                                        <>
                                            <Button
                                                variant='primary'
                                                fontType='fW600 fS18 secondary'
                                                onClick={() =>
                                                    handleUpdateRates(
                                                        commission?.service_type
                                                    )
                                                }>
                                                Update
                                            </Button>
                                            <Button
                                                variant='transparent'
                                                fontType='fW600 fS18 secondary'
                                                onClick={() =>
                                                    handleEditClick(
                                                        commission?.service_type
                                                    )
                                                }>
                                                Cancel
                                            </Button>
                                        </>
                                    ) : (
                                        <Icon
                                            onClick={() =>
                                                handleEditClick(
                                                    commission?.service_type
                                                )
                                            }
                                            src={edit}
                                            className='commission-rates-edit-icon'
                                        />
                                    )}
                                </div>
                            </Card>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default CommissionRates;
