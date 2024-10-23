// React imports
import React from "react";
// import { useState } from 'react'
// Import react props //
import { HashRouter as Router, Routes, Route, Navigate } from "react-router-dom";
// Import some materials utilities
import { ThemeProvider, CssBaseline } from '@mui/material';
// Include the snackbar from MUI
import { SnackbarProvider } from 'notistack'
// Pages imports
import Home from "./pages";
import NotFound from "./pages/not_found";
import CashierData from "./pages/interface/cashier";
import ClientData from "./pages/interface/client";
import ProblemPage from "./pages/interface/problem";
import FaqPage from "./pages/interface/faq";
// Other Local imports
import { theme } from "./theme";

// Add the 

function App() {
  // Set the open sidebar section (and close sidebar)
  const [open, setOpen] = React.useState(true);
  // Return the routes section for the page
  return (
    <ThemeProvider theme={theme()}>
      <CssBaseline />
      <div className="app">
        <SnackbarProvider />
        <main className="content">
          <Router basename="/">
            <Routes>
              {/* Route for the index page*/}
              <Route
                path="/"
                element={<Home />}
              />
              {/* Import the 404 route */}
              <Route
                path="*"
                element={<NotFound open={open} setOpen={setOpen} />}
              />
              {/* ============================= */}
              {/* Interfaces PAGES */}
              <Route path="/interface" element={<Navigate to="/interface/cashier_data" />} />
              <Route path="/interface/cashier_data" element={<CashierData open={open} setOpen={setOpen} />} />
              <Route path="/interface/clients" element={<ClientData open={open} setOpen={setOpen} />} />
              <Route path="/interface/run" element={<ProblemPage open={open} setOpen={setOpen} />} />
              <Route path="/interface/faq" element={<FaqPage open={open} setOpen={setOpen} />} />
            </Routes>
          </Router>
        </main>
      </div>
    </ThemeProvider>
  )
}

export default App;
