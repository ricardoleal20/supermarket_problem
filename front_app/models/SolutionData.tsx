// Cashier model, to receive data from it
// and to manage easily the data
import { GridColDef, GridRowId } from '@mui/x-data-grid';
// Icons
import BadgeOutlinedIcon from '@mui/icons-material/BadgeOutlined';
import WatchOutlinedIcon from '@mui/icons-material/WatchOutlined';
import ShoppingCartOutlinedIcon from '@mui/icons-material/ShoppingCartOutlined';
import NumbersOutlinedIcon from '@mui/icons-material/NumbersOutlined';
// Local imports
import { DataTableModel } from "../components/DataTable"
import { Typography } from '@mui/material';
import { Box } from '@mui/material';

function arrivalTimeToDate(arrivalTime: number): string {
    const baseHour = 8;
    // Get the hours and minutes
    const hours = baseHour + Math.floor(arrivalTime / 60);
    const minutes = arrivalTime % 60;
    // Modify the final parameters
    const timeOfDay = hours < 12 ? "AM" : "PM";
    const hoursString = hours < 13 ? `${hours}` : `${hours - baseHour}`;
    const minutesString = minutes < 10 ? `0${minutes}` : `${minutes}`;
    // Get the last hour
    return `${hoursString}:${minutesString} ${timeOfDay}`;
}

interface SolutionDataInterface {
    /// This interface allow me to define what are I'm going to need
    /// for this model
    workerId: string,
    serviceLevel: number,
    waitingTime: number,
    processingTime: number,
    freeTime: number,
}

export default class CashierPerformance implements DataTableModel, SolutionDataInterface {
    /// This class is just the object to retrieve the data
    constructor(
        public id: GridRowId,
        public workerId: string,
        public serviceLevel: number,
        public waitingTime: number,
        public processingTime: number,
        public freeTime: number
    ) { }

    // Method to return the columns from the model
    private static getFieldsInformation(): GridColDef[] {
        return [
            // Hide the ID column
            { field: "id", headerName: "ID" },
            {
                field: 'workerId',
                headerName: 'Worker ID',
                type: "string",
                // width: 200,
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <BadgeOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Cashier
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<BadgeOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
            },
            {
                field: 'serviceLevel',
                headerName: 'Service Level',
                type: "number",
                sortable: true,
                // width: 200,
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center" justifyContent="center" style={{ width: '100%' }}>
                            <WatchOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Service Level
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<WatchOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
            },
            {
                field: 'waitingTime',
                headerName: 'Waiting Time',
                type: "string",
                sortable: true,
                // width: 200,
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center" justifyContent="center" style={{ width: '100%' }}>
                            <WatchOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Waiting Time
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<WatchOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
            },
            {
                field: 'processingTime',
                headerName: 'Processing Time',
                type: "string",
                sortable: true,
                // width: 200,
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center" justifyContent="center" style={{ width: '100%' }}>
                            <WatchOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Processing Time
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<WatchOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
            },
            {
                field: 'freeTime',
                headerName: 'Free Time in shift',
                type: "number",
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <ShoppingCartOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Free Time
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<ShoppingCartOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
            },
        ];
    }

    getFieldsInfo() {
        return CashierPerformance.getFieldsInformation();
    }

    static getFieldsInfo() {
        return CashierPerformance.getFieldsInformation();
    }
}
