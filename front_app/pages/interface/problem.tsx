/// * Problem page.
/// *
/// * This page would include the
/// * interface to run the problem, along with some plots
/// * to show the results from the problem.
// ===========================
// React imports
import React from 'react';
// Include the alerts
import { enqueueSnackbar } from 'notistack'
// MUI imports
import { Box, Typography, Divider } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import CalculateOutlinedIcon from '@mui/icons-material/CalculateOutlined';
// Local imports
import KPICard from '../../components/KPICard';
import { PageTemplate, AvailablePages, PageChildrenProps } from "../../components/PageTemplate";
import { colorTokens } from '../../theme';
import { performRequest } from '../../utils';



const ProblemPage: React.FC<PageChildrenProps> = ({ open, setOpen }) => {
    // Get the colors
    const colors = colorTokens();
    // Get the state for the loading button
    const [loadingRunButton, setLoadingRunButton] = React.useState(false);
    // Get the solution data
    const [solutionData, setSolutionData] = React.useState([]);

    // Define the method to handle the execution of the problem
    const handleRunProblem = async () => {
        setLoadingRunButton(true);
        // First of all, check if we have the cashier data on the session storage
        const cashierData = JSON.parse(sessionStorage.getItem('cashierData') || "[]");
        if (cashierData.length === 0) {
            // Show an alert saying that the data was confirmed
            enqueueSnackbar(
                <Typography>
                    There's no <strong>Cashier data</strong> to use to solve the problem. Please go to its page and confirm the data.
                </Typography>,
                {
                    variant: 'error',
                    autoHideDuration: 3000,
                    preventDuplicate: true,
                    anchorOrigin: { horizontal: "center", vertical: "bottom" },
                    style: {
                        backgroundColor: colors.redAccent[800],
                    }
                });
            setLoadingRunButton(false);
            return;
        }
        // Do the same for the clientData
        const clientData = JSON.parse(sessionStorage.getItem('clientData') || "[]");
        if (clientData.length === 0) {
            // Show an alert saying that the data was confirmed
            enqueueSnackbar(
                <Typography>
                    There's no <strong>Client data</strong> to use to solve the problem. Please go to its page and confirm the data.
                </Typography>,
                {
                    variant: 'error',
                    autoHideDuration: 3000,
                    preventDuplicate: true,
                    anchorOrigin: { horizontal: "center", vertical: "bottom" },
                    style: {
                        backgroundColor: colors.redAccent[800],
                    }
                });
            setLoadingRunButton(false);
            return;
        }
        // Then, if we have the data for it, run the problem!
        await new Promise(resolve => setTimeout(resolve, 1500));
        const data = await performRequest("solve_problem", "POST", {
            "cashiers": cashierData,
            "clients": clientData,
        });
        console.log("Data is...", data);
        await new Promise(resolve => setTimeout(resolve, 1500));
        setSolutionData(data);
        setLoadingRunButton(false);
    }

    // Generate the button for the hader
    const ButtonHeader = (
        <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: "0em" }}>
            <Box component="form" sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', gap: '1em' }}>
                <LoadingButton
                    variant="contained"
                    loading={loadingRunButton}
                    loadingPosition="start"
                    startIcon={<CalculateOutlinedIcon />}
                    onClick={handleRunProblem}
                    sx={{ backgroundColor: colors.greenAccent[800] }}
                >
                    RUN SOLVER
                </LoadingButton>
            </Box>
        </Box>
    );


    return (
        <PageTemplate
            page={AvailablePages.RunSolver}
            open={open}
            setOpen={setOpen}
            customButtonHeader={ButtonHeader}
        >
            {/* If we do no have data, we'll show a message saying that we don't have it and asking to run the solver */}
            {solutionData.length === 0 ? (
                <Box alignItems="center" marginTop="2em">
                    <Divider />
                    <Typography variant="h5" margin="3em" align='center' color={colors.grey[300]}>
                        There's no solution data to show. Please run the solver to get the results.
                    </Typography>
                    <Divider />
                </Box>
            ) : (
                <>
                    {/* If we have data, we'll show the results. */}
                    {/* ======================================== */}
                    {/*                  KPIs                    */}
                    {/* ======================================== */}
                    <Box display="flex" justifyContent="space-around" marginTop="2em">
                        <KPICard title="Average Queue Waiting Time" value={"1"} description="How much minutes do each client wait on the queue to start being processed?" />
                        <KPICard title="Average Processing Time" value={"1"} description="How much minutes do each client takes to get into the queue and to be processed?" />
                        <KPICard title="Average free-time on the cashiers" value={"1"} description="Average dead-time between the cashiers" />
                        <KPICard title="Service Level" value={"1"} description="Clients processed in less than 3 minutes since they arrive to the queue" />
                    </Box>
                    {/* ======================================== */}
                    {/*                  GANTT                   */}
                    {/* ======================================== */}

                    {/* ======================================== */}
                    {/*                  OTHERS                  */}
                    {/* ======================================== */}
                </>
            )}
        </PageTemplate>
    )
}

export default ProblemPage;
