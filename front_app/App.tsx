// React imports
import React, { useEffect } from "react";
// import { useState } from 'react'
// Import react props //
import { HashRouter as Router, Routes, Route, Navigate } from "react-router-dom";
// Import some materials utilities
import { ThemeProvider, CssBaseline } from '@mui/material';
// Include the snackbar from MUI
import { SnackbarProvider, enqueueSnackbar } from 'notistack'
// Pages imports
import Home from "./pages";
import NotFound from "./pages/not_found";
import CashierData from "./pages/interface/cashier";
import ClientData from "./pages/interface/client";
import ProblemPage from "./pages/interface/problem";
import FaqPage from "./pages/interface/faq";
// Other Local imports
import { theme } from "./theme";
import { performRequest } from "./utils";

function sendAlert() {
  enqueueSnackbar(
    'The backend is initializing. If an action keeps loading, please reload.',
    {
      variant: 'info',
      autoHideDuration: 3000,
      preventDuplicate: true,
      anchorOrigin: { horizontal: "center", vertical: "bottom" },
    })
}


function App() {
  // Perform a request to the home backend page. What we're waiting
  // is that the backend is up and running. If we do not receive a response
  // in a certain amount of time, we can assume that the backend is not running
  // and we can show a message to the user.
  useEffect(() => {
    const checkBackendStatus = async () => {
      try {
        const response = await performRequest("", "GET");
        if (!response.serverRunning) {
          sendAlert();
        }
      } catch (error) {
        sendAlert();
      }
    };

    checkBackendStatus();
  }, []);
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
