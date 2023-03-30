import { capitalize } from "@mui/material";
import { Spinner, Table } from "react-bootstrap";
import Header from "../../components/header/Header";

const PaymentsTable = ({ columns, content, isLoading, customCell }) => {
    const paymentStatus = {
        NOT_PAID: "Pending",
        PAID: "Paid",
    };
    const getTableCell = (column, paymentInfo) => {
        switch (column) {
            case "Agent Name":
                return paymentInfo?.agent_name ?? "-";
            case "Amount":
                return `£ ${paymentInfo?.amount}` ?? "-";
            case "Payment due":
                return (
                    new Date(paymentInfo?.pay_date).toLocaleDateString(
                        "en-US",
                        {
                            year: "numeric",
                            month: "short",
                            day: "numeric",
                        }
                    ) ?? "-"
                );
            case "Status":
                return paymentStatus[paymentInfo?.status] ?? "-";
            case "Type":
                return (
                    capitalize(String(paymentInfo?.type?.toLowerCase())) ?? "-"
                );
            case "custom":
                return customCell(paymentInfo);
            default:
                return "-";
        }
    };
    return (
        <div className='payments-table-container'>
            {isLoading ? (
                <Spinner />
            ) : (
                <Table striped className='payments-table'>
                    <thead>
                        <tr>
                            {columns.map((columnValue, key) => (
                                <th
                                    key={`${key}-service-head`}
                                    className='payments-column-head'>
                                    <Header
                                        type='fS21 tertiary fW600'
                                        className='payments-column'>
                                        {columnValue === "custom"
                                            ? ""
                                            : columnValue}
                                    </Header>
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {content.length <= 0 ? (
                            <tr>
                                <td colSpan={columns.length}>
                                    <Header
                                        type='fW600 fS28 primary'
                                        className='payments-empty-row'>
                                        No payments to display
                                    </Header>
                                </td>
                            </tr>
                        ) : (
                            content.map((payment, key) => (
                                <tr
                                    key={`${key}-tr-service`}
                                    className='payments-row'>
                                    {columns.map((item, cellKey) => (
                                        <td
                                            className='payments-cell'
                                            key={`${key}${cellKey}-ts-cell`}>
                                            <Header
                                                type={`fW400 fS18 ${
                                                    item !== "Status"
                                                        ? "tertiary"
                                                        : payment?.status ===
                                                          "NOT_PAID"
                                                        ? "error"
                                                        : "primary"
                                                }`}>
                                                {getTableCell(item, payment)}
                                            </Header>
                                        </td>
                                    ))}
                                </tr>
                            ))
                        )}
                    </tbody>
                </Table>
            )}
        </div>
    );
};

export default PaymentsTable;
