//*  Cashier Page
// *
// * This page contains a datatable with the configuration to send for the user to pre-define the
// * available cashiers in the project, being these the ones that we're going to send to the
// * backend to perform the calculations in our pre-made model.
// ===========================
// React imports
// Material UI imports
import { Box, Typography } from "@mui/material";
// Local improts
import Sidebar from "../../components/SideBar";

const CashierData = () => {
    return (
        <Box>
            {/* Initialize the Sidebar */}
            <Sidebar />
            <Box component="main" sx={{ flexGrow: 1, padding: 3 }}>
                <Typography variant="h1">TEST</Typography>
            </Box>
        </Box>
    )
}

export default CashierData;