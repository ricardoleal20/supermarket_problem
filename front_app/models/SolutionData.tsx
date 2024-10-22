// Cashier model, to receive data from it
// and to manage easily the data
import { GridRowId } from '@mui/x-data-grid';
// Icons
import BadgeOutlinedIcon from '@mui/icons-material/BadgeOutlined';
import WatchOutlinedIcon from '@mui/icons-material/WatchOutlined';
import ShoppingCartOutlinedIcon from '@mui/icons-material/ShoppingCartOutlined';
// Local imports
import { DataTableModel, FieldsInfo } from "../components/DataTable"
import { Typography } from '@mui/material';
import { Box } from '@mui/material';

export default class CashierPerformance implements DataTableModel {
    id: GridRowId;
    workerId: string;
    serviceLevel: number;
    waitingTime: number;
    processingTime: number;
    freeTime: number;

    /// This class is just the object to retrieve the data
    constructor(
        id: GridRowId,
        workerId: string,
        serviceLevel: number,
        waitingTime: number,
        processingTime: number,
        freeTime: number
    ) {
        this.id = id;
        this.workerId = workerId;
        this.serviceLevel = serviceLevel;
        this.waitingTime = waitingTime;
        this.processingTime = processingTime;
        this.freeTime = freeTime;
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
