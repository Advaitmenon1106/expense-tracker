import { Link, Outlet } from 'react-router-dom';
import './ExpenseOperations.css'
import { MenuTab } from '../Expense_Analysis/ExpenseAnalysis';


export function ExpenseOperations() {
    return (
        <div className="analysis-page">

            <div id="all-menus">
                <Link to="add-single">
                    <MenuTab menuDisplay="Add an expense" />
                </Link>

                <Link to="statement-upload">
                    <MenuTab menuDisplay="Upload a bank statement" />
                </Link>
            </div>

            <div className="content-area">
                <Outlet />
            </div>

        </div>
    );
}
