// Cashier model, to receive data from it
// and to manage easily the data
import { GridColDef, GridRowId } from '@mui/x-data-grid';
// Icons
import BadgeOutlinedIcon from '@mui/icons-material/BadgeOutlined';
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined';
import ModeNightOutlinedIcon from '@mui/icons-material/ModeNightOutlined';
import PercentOutlinedIcon from '@mui/icons-material/PercentOutlined';
// Local imports
import { DataTableModel } from "../components/DataTable"
import { Typography } from '@mui/material';
import { Box } from '@mui/material';

interface CashierInterface {
    /// This interface allow me to define what are I'm going to need
    /// for this model
    workerId: string;
    available_in_the_morning: boolean;
    available_in_the_afternoon: boolean;
    effectiveness_average: number;
}

export default class Cashier implements DataTableModel, CashierInterface {
    /// This class is just the object to retrieve the data
    constructor(
        public id: GridRowId,
        public workerId: string,
        public available_in_the_morning: boolean,
        public available_in_the_afternoon: boolean,
        public effectiveness_average: number
    ) { }

    // Method to return the columns from the model
    private static getColumns(): GridColDef[] {
        return [
            // Hide the ID column
            { field: "id", headerName: "ID" },
            {
                field: 'workerId',
                headerName: 'Worker ID',
                type: "string",
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <BadgeOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Worker ID
                        </Box>
                    </Typography>
                )
            },
            {
                field: 'available_in_the_morning',
                headerName: 'Available in the morning',
                type: "boolean",
                width: 200,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <LightModeOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Available in the morning
                        </Box>
                    </Typography>
                )
            },
            {
                field: 'available_in_the_afternoon',
                headerName: 'Available in the afternoon',
                type: "boolean",
                width: 200,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <ModeNightOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Available in the afternoon
                        </Box>
                    </Typography>
                )
            },
            {
                field: 'effectiveness_average',
                headerName: 'Effectiveness Average',
                type: "number",
                width: 200,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <PercentOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Effectiveness Average
                        </Box>
                    </Typography>
                )
            },
        ];
    }

    generateColumns() {
        return Cashier.getColumns();
    }

    static generateColumns() {
        return Cashier.getColumns();
    }
}
