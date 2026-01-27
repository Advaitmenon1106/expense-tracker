import './Sidebar.css'

export function Sidebar() {
    const menu_options = ["Home", "Add Expenses", "Analyse", "Assistant"]

    return (
        <div id="sidebar">
            {menu_options.map((option) => {
                return <div key={option} className="sidebar-options">{option}</div>
            })}
        </div>
    )
}