// Cashier model, to receive data from it
// and to manage easily the data

// Include the UUID4 generator
import { v4 as uuidv4 } from 'uuid';
import { GridRowId } from '@mui/x-data-grid';
// Icons
import WatchOutlinedIcon from '@mui/icons-material/WatchOutlined';
import ShoppingCartOutlinedIcon from '@mui/icons-material/ShoppingCartOutlined';
import NumbersOutlinedIcon from '@mui/icons-material/NumbersOutlined';
// Local imports
import { DataTableModel, FieldsInfo } from "../components/DataTable"
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

interface ClientInterface {
    /// This interface allow me to define what are I'm going to need
    /// for this model
    clientId: string
    arrivalTime: number
    products: number
}

export default class Client implements DataTableModel, ClientInterface {
    /// This class is just the object to retrieve the data
    id: GridRowId;
    clientId: string;
    arrivalTime: number;
    products: number

    constructor(
        clientId: string,
        arrivalTime: number,
        products: number
    ) {
        this.id = clientId;
        this.clientId = clientId;
        this.arrivalTime = arrivalTime;
        this.products = products;
    }

    // Method to return the columns from the model
    private static getFieldsInformation(): FieldsInfo[] {
        return [
            // Hide the ID column
            { field: "id", headerName: "ID" },
            {
                field: 'clientId',
                headerName: 'Client ID',
                type: "number",
                // width: 200,
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <NumbersOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Client ID
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<NumbersOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
            },
            {
                field: 'arrivalTime',
                headerName: 'Arrival Date',
                type: "string",
                sortable: true,
                // width: 200,
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center" justifyContent="center" style={{ width: '100%' }}>
                            <WatchOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Arrival Date
                        </Box>
                    </Typography>
                ),
                renderCell: (params) => (
                    <Typography>
                        <Box display="flex" alignItems="center" justifyContent="center" style={{ width: '100%', height: '100%' }}>
                            {arrivalTimeToDate(params.row.arrivalTime)}
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<WatchOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
            },
            {
                field: 'products',
                headerName: 'Quantity of products',
                type: "number",
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <ShoppingCartOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Quantity of products
                        </Box>
                    </Typography>
                ),
                labelIcon: () => (<ShoppingCartOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} />),
                rangeValues: { min: 0.1, max: 1.0 },
            },
        ];
    }

    getFieldsInfo() {
        return Client.getFieldsInformation();
    }

    static getFieldsInfo() {
        return Client.getFieldsInformation();
    }

    static id: GridRowId = new Client(uuidv4(), 0, 0).id;
}
