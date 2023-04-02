import { PAGE_HEADER_TYPE } from "../../constants/header_types";
import "./payments.scss";
import Header from "../../components/header/Header";
import Tab from "../../components/tab/Tab";
import PaymentsTable from "./PaymentsTable";
import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState } from "react";
import {
    fetchAllPaymentsAsync,
    fetchUserPaymentsAsync,
    updateSinglePaymentAsync,
} from "../../api/paymentsApi";
import {
    updatePaidPayments,
    updateUnpaidPayments,
} from "../../redux/payments/paymentReducer";
import Button from "../../components/button/Button";
import { ADMIN } from "../../constants/user_roles";

const Payments = () => {
    const dispatch = useDispatch();
    const [paidPayments, unpaidPayments, userId, userRole] = useSelector(
        (states) => [
            states?.payments?.paidPayments ?? [],
            states?.payments?.unpaidPayments ?? [],
            states?.users?.userDetails?.userId,
            states?.users?.userDetails?.role,
        ]
    );

    const [isLoading, setLoading] = useState(false);

    const setupPayments = async () => {
        let paidRes,
            unpaidRes = [];
        if (userRole === ADMIN) {
            unpaidRes = await fetchAllPaymentsAsync("NOT_PAID", userId);
            paidRes = await fetchAllPaymentsAsync("PAID", userId);
        } else {
            unpaidRes = await fetchUserPaymentsAsync("NOT_PAID", userId);
            paidRes = await fetchUserPaymentsAsync("PAID", userId);
        }
        dispatch(updatePaidPayments(paidRes ?? []));
        dispatch(updateUnpaidPayments(unpaidRes ?? []));

        setTimeout(() => setLoading(false), 1500);
    };

    useEffect(() => {
        if (userId) {
            setLoading(true);
            setupPayments();
        }
    }, [userId]);

    const handlePayAgent = async (data) => {
        let res = await updateSinglePaymentAsync(
            userId,
            data?.agent_id,
            data?.id
        );
        if (res?.includes("Success")) {
            setupPayments();
        }
    };

    const payBtn = (data) => (
        <Button
            variant='primary'
            fontType='fS18 fW600 secondary'
            onClick={() => handlePayAgent(data)}>
            Pay
        </Button>
    );

    const agent_cols = ["Amount", "Type", "Payment due", "Status"];
    const columns = [
        "Agent Name",
        "Amount",
        "Type",
        "Payment due",
        "Status",
        "custom",
    ];
    const paidCols = ["Agent Name", "Amount", "Type", "Payment due", "Status"];

    const paymentTab = [
        {
            key: "UNPAID",
            title: "Pending payments",
            content: (
                <PaymentsTable
                    content={unpaidPayments}
                    isLoading={isLoading}
                    columns={userRole === ADMIN ? columns : agent_cols}
                    customCell={payBtn}
                />
            ),
        },
        {
            key: "PAID",
            title: "Paid payments",
            content: (
                <PaymentsTable
                    content={paidPayments}
                    isLoading={isLoading}
                    columns={userRole === ADMIN ? paidCols : agent_cols}
                />
            ),
        },
    ];
    return (
        <div className='payments'>
            <div className='payments-header'>
                <Header
                    type={PAGE_HEADER_TYPE}
                    className='payments-header-title'>
                    Agent Payments
                </Header>
            </div>
            <div className='payments-body'>
                <Tab tabs={paymentTab} className='payments-tab' />
            </div>
        </div>
    );
};

export default Payments;
