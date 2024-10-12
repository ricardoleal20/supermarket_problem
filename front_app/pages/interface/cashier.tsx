//*  Cashier Page
// *
// * This page contains a datatable with the configuration to send for the user to pre-define the
// * available cashiers in the project, being these the ones that we're going to send to the
// * backend to perform the calculations in our pre-made model.
// ===========================
// React imports
// Mui imports
import Typography from '@mui/material/Typography';
// Local improts
import { PageTemplate, AvailablePages, PageChildrenProps } from "../../components/PageTemplate";
import { DataTable } from '../../components/DataTable';
import { useState } from 'react';
import { Cashier } from '../../models';


const rawData: Cashier[] = [
    new Cashier(1, 'W001', true, false, 0.8),
    new Cashier(2, 'W002', true, true, 0.9),
    new Cashier(3, 'W003', false, true, 0.7),
    new Cashier(4, 'W004', false, false, 0.95),
];

const CashierData: React.FC<PageChildrenProps> = ({ open, setOpen }) => {

    // Get the data
    const [data, setData] = useState(rawData);

    return (
        <PageTemplate
            page={AvailablePages.CashierData}
            open={open}
            setOpen={setOpen}
        >
            <Typography variant="h4">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure
                dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
                proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </Typography>
            {/* Add the table for the cashier data */}
            <DataTable
                model={Cashier}
                data={data}
                setData={setData}
                isEditable={true}
            />
        </PageTemplate>
    )
}

export default CashierData;