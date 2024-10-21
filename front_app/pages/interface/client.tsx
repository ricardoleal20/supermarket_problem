//*  Cashier Page
// *
// * This page contains a datatable with the configuration to send for the user to pre-define the
// * available cashiers in the project, being these the ones that we're going to send to the
// * backend to perform the calculations in our pre-made model.
// ===========================
// React imports
import React from 'react';
// Mui imports
import Typography from '@mui/material/Typography';
// Local improts
import { PageTemplate, AvailablePages, PageChildrenProps } from "../../components/PageTemplate";
import { DataTable } from '../../components/DataTable';
import { useState } from 'react';
import { Client } from '../../models';
// Include the accordion for information about the model
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
// Include some icons
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DataArrayOutlinedIcon from '@mui/icons-material/DataArrayOutlined';
import DeleteOutlineOutlinedIcon from '@mui/icons-material/DeleteOutlineOutlined';
// Include the buttons section
import { TextField, Box, Divider, Button } from '@mui/material';
import LoadingButton from '@mui/lab/LoadingButton';
// Include the alerts
import { enqueueSnackbar } from 'notistack'
// Local imports
import { colorTokens } from '../../theme';
import { performRequest } from '../../utils';


const rawData: Client[] = [];

// Define the children props for the cleint data, using as base the pageChildren Props
const ClientData: React.FC<PageChildrenProps> = ({ open, setOpen }) => {
    const colors = colorTokens();
    // Get the data
    // * First, if the data exist on the session storage, then we can
    // * use it as the base data for the table
    const clientData = JSON.parse(sessionStorage.getItem('clientData') || "[]");

    const [data, setData] = useState(clientData.length > 0 ? clientData : rawData);
    // Select if the accordion is expanded or not
    const [expanded, setExpanded] = React.useState(false);
    const [expandedSecondAccordion, setExpandedSecond] = React.useState(false);
    // Create the state to handle the alert show

    const handleExpansion = () => {
        setExpanded((prevExpanded) => !prevExpanded);
    };


    const handleExpansionSecond = () => {
        setExpandedSecond((prevExpanded) => !prevExpanded);
    };

    // Define the morning and afternoon variance
    const [morningVariance, setMorningVariance] = useState(15);
    const [afternoonVariance, setAfternoonVariance] = useState(15);
    // Define the loading state for the buttons
    const [loadingCreateDataButton, setLoadingCreateDataButton] = useState(false);
    const [loadingDeleteButton, setLoadingDeleteButton] = useState(false);

    // Define the method to confirm the data
    const handleConfirmData = () => {
        // Show an alert saying that the data was confirmed
        enqueueSnackbar('Data confirmed', {
            variant: 'success',
            autoHideDuration: 3000,
            preventDuplicate: true,
            anchorOrigin: { horizontal: "center", vertical: "bottom" },
            style: {
                backgroundColor: colors.greenAccent[800],
            }
        });
        // Then, store the data in the session storage
        sessionStorage.setItem('clientData', JSON.stringify(data));
    };

    // Define the method to generate the random data
    const handleGenerateRandomData = async () => {
        // Set the loading state as true
        setLoadingCreateDataButton(true);
        // Get the data 
        const data = await performRequest("generate_clients", "POST", {
            "morning_variance": morningVariance,
            "afternoon_variance": afternoonVariance,
        })
        // Convert the array of data to the expected type
        const clients: Client[] = data.map((client: any) => {
            return {
                id: client.id,
                clientId: client.id,
                arrivalTime: client.arrival_time,
                products: client.products,
            }
        });
        // Sort the clients by the arrivalTime
        clients.sort((a, b) => a.arrivalTime - b.arrivalTime);
        // Set the data and quit the loading state
        setTimeout(() => {
            setData(clients);
            setLoadingCreateDataButton(false);
        }, 1500);
    }

    const handleCleanData = () => {
        setLoadingDeleteButton(true);
        // Wait for 2 seconds
        setTimeout(() => {
            // Just set the new data to something empty
            setData([]);
            setLoadingDeleteButton(false);
        }, 1500);
    }

    // Create the custom button header here
    const ButtonHeader = (
        <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: "0em" }}>
            <Box component="form" sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', gap: '1em' }}>
                <TextField
                    label="Morning Variance"
                    variant="outlined"
                    type="number"
                    inputProps={{ min: 10, max: 50, step: 1 }}
                    value={morningVariance}
                    onChange={(e) => setMorningVariance(parseFloat(e.target.value))}
                    sx={{ minWidth: "8em" }}
                />
                <TextField
                    label="Afternoon Variance"
                    variant="outlined"
                    type="number"
                    inputProps={{ min: 0, max: 2, step: 0.1 }}
                    value={afternoonVariance}
                    onChange={(e) => setAfternoonVariance(parseFloat(e.target.value))}
                    sx={{ minWidth: "8.5em" }}
                />
                <LoadingButton
                    loadingPosition="start"
                    variant="contained"
                    loading={loadingCreateDataButton}
                    startIcon={<DataArrayOutlinedIcon />}
                    onClick={handleGenerateRandomData}
                >
                    Generate Data
                </LoadingButton>
                <Typography variant="h1">
                    |
                </Typography>
                <LoadingButton
                    loadingPosition="start"
                    variant="contained"
                    loading={loadingDeleteButton}
                    startIcon={<DeleteOutlineOutlinedIcon />}
                    onClick={handleCleanData}
                >
                    Clean data
                </LoadingButton>
                <Typography variant="h1">
                    |
                </Typography>
                <Button
                    variant="contained"
                    // loading={loadingDeleteButton}
                    // startIcon={<DeleteOutlineOutlinedIcon />}
                    onClick={handleConfirmData}
                    sx={{ backgroundColor: colors.greenAccent[800] }}
                >
                    CONFIRM DATA
                </Button>
            </Box>
        </Box>
    );

    return (
        <PageTemplate
            page={AvailablePages.Clients}
            open={open}
            setOpen={setOpen}
            customButtonHeader={ButtonHeader}
        >
            <Typography variant="h5">
                Generate a list of clients. For that, we can fill it manually or generate it randomly.
                For the random generation, we'll use the buttons on the header to define the variance for both shifts.
            </Typography>
            {/* Add the buttons to generate the data */}

            {/* Add the table for the Client data */}
            <DataTable
                model={Client}
                data={data}
                setData={setData}
                isEditable={true}
            />
            {/* Include the accordion with information about each parameter of the Client */}
            <Accordion
                expanded={expanded}
                onChange={handleExpansion}
                slotProps={{ transition: { timeout: 400 } }}
                sx={[
                    { marginTop: "1em" },
                    expanded
                        ? {
                            '& .MuiAccordion-region': {
                                height: 'auto',
                            },
                            '& .MuiAccordionDetails-root': {
                                display: 'block',
                            },
                        }
                        : {
                            '& .MuiAccordion-region': {
                                height: 0,
                            },
                            '& .MuiAccordionDetails-root': {
                                display: 'none',
                            },
                        },
                ]}
            >
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel1-content"
                    id="panel1-header"
                >
                    <Typography>Detailed information about each column</Typography>
                </AccordionSummary>
                <Divider />
                <AccordionDetails>
                    <Typography variant="h6">
                        <ul>
                            <li>
                                <strong>Client ID:</strong> The ID of the client. Just as a reference for the results.
                            </li>
                            <li>
                                <strong>Arrival Date:</strong> The date of arrival to the queue. It's a string with the format "HH:MM".
                            </li>
                            <li>
                                <strong>Quantity of products:</strong> How much products the client is going to buy. It's a number between 1 and 50. For each product, we take in average, 15 seconds to process it.
                            </li>
                        </ul>
                    </Typography>
                </AccordionDetails>
            </Accordion>
            {/* Add another accordion with the information about the model */}
            <Accordion
                expanded={expandedSecondAccordion}
                onChange={handleExpansionSecond}
                slotProps={{ transition: { timeout: 400 } }}
                sx={[
                    { marginTop: "1em" },
                    expandedSecondAccordion
                        ? {
                            '& .MuiAccordion-region': {
                                height: 'auto',
                            },
                            '& .MuiAccordionDetails-root': {
                                display: 'block',
                            },
                        }
                        : {
                            '& .MuiAccordion-region': {
                                height: 0,
                            },
                            '& .MuiAccordionDetails-root': {
                                display: 'none',
                            },
                        },
                ]}
            >
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel1-content"
                    id="panel2-header"
                >
                    <Typography>Detailed information about the variance</Typography>
                </AccordionSummary>
                <Divider />
                <AccordionDetails>
                    <Typography variant="h6">
                        The variance, for this model, is how many clients we do expect to find in each
                        shift, and how far is going to be from an specific time. In this case:
                        <ul>
                            <li>
                                <strong>Morning variance:</strong> The variance for the morning shift.
                            </li>
                            <li>
                                <strong>Afternoon variance:</strong> The variance for the afternoon shift.
                            </li>
                        </ul>
                    </Typography>
                </AccordionDetails>
            </Accordion>
        </PageTemplate>
    )
}

export default ClientData;