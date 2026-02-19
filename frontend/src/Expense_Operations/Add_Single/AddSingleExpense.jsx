import './AddSingleExpense.css'
import { useState } from 'react';


export function AddSingleExpense() {
    const expenseFormFields = [
        {
            name: "expense_name",
            label: "Cashflow name",
            type: "text",
            required: true
        },
        {
            name: "amount",
            label: "Amount",
            type: "number",
            required: true
        },
        {
            name: "date",
            label: "Date",
            type: "date",
            required: true
        },
        {
            name: "inflow",
            label: "Is this an inflow?",
            type: "checkbox",
            required: true
        },
        {
            name: "tags",
            label: "Tags",
            type: "text",
            required: false
        },
        {
            name: "remarks",
            label: "Remarks",
            type: "text",
            required: false
        }
    ];

    const [formData, setFormData] = useState({
        expense_name: "",
        amount: "",
        date: "",
        inflow: false,
        tags: "",
        remarks: ""
    });


    const handleSubmit = async (e) => {
        e.preventDefault();

        const params = new URLSearchParams({
            expense_name: formData.expense_name,
            amount: Number(formData.amount),
            date: formData.date,
            inflow: formData.inflow,
            tags: formData.tags || "",
            remarks: formData.remarks || ""
        });

        const response = await fetch(
            `http://0.0.0.0:8000/insert-expense?${params.toString()}`,
            {
                method: "POST"
            }
        );

        if (!response.ok) {
            console.error("Failed to submit expense");
            return;
        }

        const result = await response.json();
        console.log("Expense inserted:", result);
    };

    const handleChange = (e) => {
        const { name, type, value, checked } = e.target;

        setFormData((prev) => ({
            ...prev,
            [name]: type === "checkbox" ? checked : value
        }));
    };

    return (
        <form id="form" onSubmit={handleSubmit}>
            {expenseFormFields.map((field) => (
                <>
                    <div className="text-label">
                        {field.label}
                    </div>

                    <input
                        className="text-label-input"
                        type={field.type}
                        name={field.name}
                        required={field.required}
                        value={
                            field.type === "checkbox"
                                ? undefined
                                : formData[field.name]
                        }
                        checked={
                            field.type === "checkbox"
                                ? formData[field.name]
                                : undefined
                        }
                        onChange={handleChange}
                    />
                </>
            ))}
            <button type="submit" style={{ gridColumn: "1 / span 2", marginTop: "2vh" }}>Submit Expense</button>
        </form>
    );
}