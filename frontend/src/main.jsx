import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { Sidebar } from './Sidebar/Sidebar'
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom'
import { HomePage } from './Home/HomePage'
import { ExpenseOperations } from './Expense_Operations/ExpenseOperations'
import { ExpenseAnalysis } from './Expense_Analysis/ExpenseAnalysis'
import ShowAll from './Expense_Analysis/All_Expenses/ShowAll'
import { AddSingleExpense } from './Expense_Operations/Add_Single/AddSingleExpense'
import { StatementUpload } from './Expense_Operations/Statement_Upload/StatementUpload'

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <div className='app-container'>
        <Sidebar />
        <Outlet />
      </div>
    ),
    children: [
      {
        index: true,
        path: 'home',
        element: <HomePage />
      },
      {
        path: 'add-expense',
        element: <ExpenseOperations />,
        children: [
          {
            index: true,
            element: <AddSingleExpense />
          },
          {
            path: 'add-single',
            element: <AddSingleExpense />
          },
          {
            path: 'statement-upload',
            element: <StatementUpload />
          }
        ]
      },
      {
        path: 'analyse',
        element: <ExpenseAnalysis />,
        children: [
          {
            index: true,
            element: <ShowAll />
          },
          {
            index: true,
            path: 'show-all',
            element: <ShowAll />
          }
        ]
      }
    ]
  }
])


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
