import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { Sidebar } from './Sidebar/Sidebar'
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom'
import { HomePage } from './Home/HomePage'
import { ExpenseOperations } from './Expense_Operations/ExpenseOperations'
import { ExpenseAnalysis } from './Expense_Analysis/ExpenseAnalysis'


const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <>
        <Sidebar />
        <Outlet />
      </>
    ),
    children: [
      {
        index: true,
        path: 'home',
        element: <HomePage />
      },
      {
        path: 'add-expense',
        element: <ExpenseOperations />
      },
      {
        path: 'analyse',
        element: <ExpenseAnalysis />
      }
    ]
  }
])


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
