import { Link } from 'react-router-dom'
import ShowAll from './All_Expenses/ShowAll'
import './ExpenseAnalysis.css'
import { Outlet } from 'react-router-dom'


function MenuTab({ menuDisplay, onClickFn }) {
    return (
        <div className="menu-option" onClick={onClickFn}>
            {menuDisplay}
        </div>
    )
}

export function ExpenseAnalysis() {
    return (
        <div className="analysis-page">

            <div id="all-menus">
                <Link to="show-all">
                    <MenuTab menuDisplay="Show All" />
                </Link>

                <MenuTab menuDisplay="Apply Filters On Your Data" />
                <MenuTab menuDisplay="Static Analyses" />
            </div>

            <div className="content-area">
                <Outlet />
            </div>

        </div>
    );
}
