// React imports
import React from "react";
// import { useState } from 'react'
// Import react props //
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
// Import some materials utilities
import { ThemeProvider, CssBaseline } from '@mui/material';
// Pages imports
import Home from "./pages";
import NotFound from "./pages/not_found";
import CashierData from "./pages/interface/cashier";
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
        <main className="content">
          <Router>
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
            </Routes>
          </Router>
        </main>
      </div>
    </ThemeProvider>
  )
}

export default App;
