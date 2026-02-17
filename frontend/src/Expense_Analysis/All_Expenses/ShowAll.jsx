import { useEffect, useState } from "react";
import './ShowAll.css'

function ExpenseTable({ data }) {
    return (
        <div className="table-container">
            <table className="expense-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Name</th>
                        <th>Amount</th>
                        {/* <th>Type</th> */}
                        <th>Tags</th>
                        <th>Remarks</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((expense) => (
                        <tr key={expense.id}>
                            <td>{expense.date}</td>
                            <td>{expense.name}</td>
                            <td style={{ color: expense.inflow ? "#20e783" : "red" }}>
                                ₹{expense.amount.toLocaleString()}
                            </td>
                            {/* <td>{expense.inflow ? "Income" : "Expense"}</td> */}
                            <td>{expense.tags}</td>
                            <td>{expense.remarks}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default function ShowAll() {
    const [data, setData] = useState([]);

    useEffect(() => {
        async function fetchData() {
            const response = await fetch(
                "http://0.0.0.0:8000/retrieve-all-expenses"
            );
            const result = await response.json();
            setData(result);
        }

        fetchData();
    }, []);

    return <ExpenseTable data={data} />;
}