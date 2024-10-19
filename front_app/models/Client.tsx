// Cashier model, to receive data from it
// and to manage easily the data
import { GridColDef, GridRowId } from '@mui/x-data-grid';
// Icons
import WatchOutlinedIcon from '@mui/icons-material/WatchOutlined';
import ShoppingCartOutlinedIcon from '@mui/icons-material/ShoppingCartOutlined';
import NumbersOutlinedIcon from '@mui/icons-material/NumbersOutlined';
// Local imports
import { DataTableModel } from "../components/DataTable"
import { Typography } from '@mui/material';
import { Box } from '@mui/material';

interface ClientInterface {
    /// This interface allow me to define what are I'm going to need
    /// for this model
    clientId: number
    arrivalDate: string
    products: number
}

export default class Client implements DataTableModel, ClientInterface {
    /// This class is just the object to retrieve the data
    constructor(
        public id: GridRowId,
        public clientId: number,
        public arrivalDate: string,
        public products: number
    ) { }

    // Method to return the columns from the model
    private static getFieldsInformation(): GridColDef[] {
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
                field: 'arrivalDate',
                headerName: 'Arrival Date',
                type: "boolean",
                // width: 200,
                flex: 1,
                renderHeader: () => (
                    <Typography>
                        <Box display="flex" alignItems="center">
                            <WatchOutlinedIcon fontSize="small" style={{ marginRight: "0.2em" }} /> Arrival Date
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
}
