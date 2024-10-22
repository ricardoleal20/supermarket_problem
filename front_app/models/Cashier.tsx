// Cashier model, to receive data from it
// and to manage easily the data

// Include the UUID4 generator
import { v4 as uuidv4 } from 'uuid';
// Include the GridRowId
import { GridRowId } from '@mui/x-data-grid';
// Icons
import BadgeOutlinedIcon from '@mui/icons-material/BadgeOutlined';
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined';
import ModeNightOutlinedIcon from '@mui/icons-material/ModeNightOutlined';
import PercentOutlinedIcon from '@mui/icons-material/PercentOutlined';
// Local imports
import { DataTableModel, FieldsInfo } from "../components/DataTable"
import { Typography } from '@mui/material';
import { Box } from '@mui/material';

export default class Cashier implements DataTableModel {
    id: GridRowId;
    workerId: string;
    available_in_the_morning: boolean;
    available_in_the_afternoon: boolean;
    effectiveness_average: number;


    /// This class is just the object to retrieve the data
    constructor(
        workerId: string,
        available_in_the_morning: boolean,
        available_in_the_afternoon: boolean,
        effectiveness_average: number
    ) {
        this.id = workerId;
        this.workerId = workerId;
        this.available_in_the_morning = available_in_the_morning;
        this.available_in_the_afternoon = available_in_the_afternoon;
        this.effectiveness_average = effectiveness_average;
    }

    // Method to return the columns from the model
    private static getFieldsInformation(): FieldsInfo[] {
        return [
            // Hide the ID column
            { field: "id", headerName: "ID" },
            {
                field: 'workerId',
                headerName: 'Worker ID',
                type: "string",
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <BadgeOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Worker ID
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<BadgeOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
            },
            {
                field: 'available_in_the_morning',
                headerName: 'Available in the morning',
                type: "boolean",
                // width: 200,
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <LightModeOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Available in the morning
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<LightModeOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
            },
            {
                field: 'available_in_the_afternoon',
                headerName: 'Available in the afternoon',
                type: "boolean",
                // width: 200,
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <ModeNightOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Available in the afternoon
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<ModeNightOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
            },
            {
                field: 'effectiveness_average',
                headerName: 'Effectiveness Average',
                type: "number",
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <PercentOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Effectiveness Average
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<PercentOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
                rangeValues: { min: 0.1, max: 1.0 },
            },
        ];
    }

    getFieldsInfo() {
        return Cashier.getFieldsInformation();
    }

    static getFieldsInfo() {
        return Cashier.getFieldsInformation();
    }

    static id: GridRowId = new Cashier(uuidv4(), false, false, 0).id;
}
