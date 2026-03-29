import { createRoot } from 'react-dom/client'
import React from 'react'
import ReactDOM from "react-dom/client" 
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './Main.css'

createRoot(document.body).render(
  <>
  <BrowserRouter>
    <App />
  </BrowserRouter>
  </>
)
