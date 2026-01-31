import { ExpenseAnalysis } from '../Expense_Analysis/ExpenseAnalysis'
import { ExpenseOperations } from '../Expense_Operations/ExpenseOperations'
import { HomePage } from '../Home/HomePage'
import { Link } from 'react-router-dom'
import './Sidebar.css'

export function Sidebar() {
    // const menu_options = ["Home", "Add Expenses", "Analyse", "Assistant"]
    const menu_options = [
        {
            "menu_name": "Home",
            "linkto": "/home"
        },
        {
            "menu_name": "Add Expenses",
            "linkto": "/add-expense"
        },
        {
            "menu_name": "Analyse your expenses",
            "linkto": "/analyse"
        }
        // {
        //     "menu_name": "Home",
        //     "linkto": <HomePage />
        // }
    ]

    return (
        <div id="sidebar">
            {menu_options.map((option) => {
                return (
                    <Link to={option['linkto']} key={option['menu_name']}>
                        <div key={option['menu_name']} className="sidebar-options">{option['menu_name']}</div>
                    </Link>
                )
            })}
        </div>
    )
}