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
import { Cashier } from '../../models';
// Include the accordion for information about the model
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';




const rawData: Cashier[] = [
    new Cashier(1, 'W001', true, false, 0.8),
    new Cashier(2, 'W002', true, true, 0.9),
    new Cashier(3, 'W003', false, true, 0.7),
    new Cashier(4, 'W004', false, false, 0.95),
];

const CashierData: React.FC<PageChildrenProps> = ({ open, setOpen }) => {

    // Get the data
    const [data, setData] = useState(rawData);
    // Select if the accordion is expanded or not
    const [expanded, setExpanded] = React.useState(false);

    const handleExpansion = () => {
        setExpanded((prevExpanded) => !prevExpanded);
    };

    return (
        <PageTemplate
            page={AvailablePages.CashierData}
            open={open}
            setOpen={setOpen}
        >
            <Typography variant="h5">
                Select the cashiers to consider as the main processors for the clients in the final solution.
            </Typography>
            {/* Add the table for the cashier data */}
            <DataTable
                model={Cashier}
                data={data}
                setData={setData}
                isEditable={true}
            />
            {/* Include the accordion with information about each parameter of the cashier */}
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
                <AccordionDetails>
                    <Typography variant="h6">
                        <ul>
                            <li>
                                <strong>Worker ID:</strong> The ID of the worker. Just as a reference for the results.
                            </li>
                            <li>
                                <strong>Available in the morning:</strong> If the worker is available in the morning.
                                This would allow us to put clients on the morning shift (from 8 A.M. to 2 P.M.)
                            </li>
                            <li>
                                <strong>Available in the afternoon:</strong> If the worker is available in the afternoon.
                                This would allow us to put clients on the afternoon shift (from 2 P.M. to 8 P.M.)
                            </li>
                            <li>
                                <strong>Effectiveness average:</strong> The average of the effectiveness of the worker.
                                If it is higher, means that can process better the clients and their products.
                                If it is lower, means that would take it more time to attend a client.</li>
                        </ul>
                    </Typography>
                </AccordionDetails>
            </Accordion>
        </PageTemplate>
    )
}

export default CashierData;