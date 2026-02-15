import { Link } from 'react-router-dom'
import ShowAll from './All_Expenses/ShowAll'
import './ExpenseAnalysis.css'
import { useState } from 'react'


function MenuTab({ menuDisplay, onClickFn }) {
    return (
        <div className="menu-option" onClick={onClickFn}>
            {menuDisplay}
        </div>
    )
}

export function ExpenseAnalysis() {
    const [currentView, setCurrentView] = useState(null)

    const handleShowAll = async () => {
        const response = await fetch(
            `http://0.0.0.0:8000/retrieve-all-expenses`,
            {
                method: "GET"
            }
        );
        const result = await response.json();
        console.log(result);
        setCurrentView(<ShowAll data={result} />);
    }

    return (
        <div id="all-menus">
            <Link to={'/analyse/show-all'}>
                <MenuTab menuDisplay={"Show All"} onClickFn={handleShowAll} />
            </Link>

            <MenuTab menuDisplay={"Apply Filters On Your Data"} />
            <MenuTab menuDisplay={"Static Analyses"} />

            <div>
                {currentView}
            </div>
        </div>
    )
}