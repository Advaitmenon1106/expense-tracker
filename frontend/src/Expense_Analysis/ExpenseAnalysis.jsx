import './ExpenseAnalysis.css'

function MenuTab({ menuDisplay }) {
    return (
        <div className="menu-option">
            {menuDisplay}
        </div>
    )
}

export function ExpenseAnalysis() {
    return (
        <div id="all-menus">
            <MenuTab menuDisplay={"Show All"} />
            <MenuTab menuDisplay={"Apply Filters On Your Data"} />
            <MenuTab menuDisplay={"Static Analyses"} />
        </div>
    )
}