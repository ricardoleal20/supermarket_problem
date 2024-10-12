// MUI imports
import React from 'react';
import {
    DataGrid, GridColDef, GridRowsProp, GridRowModesModel,
    GridToolbarContainer, GridSlots, GridActionsCellItem,
    GridValidRowModel,
    GridRowId
} from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import { DialogTitle, DialogContent, DialogContentText, DialogActions, Dialog, TextField } from '@mui/material';
// Include the alert imports
import Stack from '@mui/material/Stack';
import Alert from '@mui/material/Alert';
// Import icons
import AddOutlinedIcon from '@mui/icons-material/Add'
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';

// Local imports

const paginationModel = { page: 0, pageSize: 5 };

// ****************** //
// Interfaces

interface HashSet<T = any> {
    [key: string]: T; // With this, i know that the entries are going to be string but the response can be anything!
}

export interface DataTableModel {
    id: GridRowId;
    generateColumns: () => GridColDef[];
}

interface DataTableProps {
    model: DataTableModel
    data: DataTableModel[],
    setData?: CallableFunction,
    isEditable?: boolean
}

interface EditToolbarProps {
    setData: (newRows: (oldData: GridRowsProp) => GridRowsProp) => void;
    setDataModesModel: (
        newModel: (oldModel: GridRowModesModel) => GridRowModesModel,
    ) => void;
    // Include the model here as well
    model: DataTableModel;
}

// ********************************************** //
// Dialog Component to add (or modify)  an item  //
// ********************************************* //

function ItemDialog(props: { open: boolean, handleClose: CallableFunction, handleSave: CallableFunction, model: DataTableModel, data?: HashSet }) {
    return (
        <Dialog open={props.open} onClose={() => props.handleClose()}>
            <DialogTitle>Item</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    Include the information for the item
                </DialogContentText>
                {/* Include automatically the fields from the model provided for the table */}
                {props.model.generateColumns().map((column) => (
                    <TextField
                        key={column.field}
                        autoFocus
                        margin="dense"
                        id={column.field}
                        label={column.headerName || column.field.charAt(0).toUpperCase() + column.field.slice(1)}
                        type={column.type || "text"}
                        fullWidth
                        variant="standard"
                        defaultValue={props.data ? props.data[column.field] : ''}
                    />
                ))}
            </DialogContent>
            <DialogActions>
                {/* Add the buttons to save or cancel the action */}
                <Button startIcon={<CancelIcon />} onClick={() => props.handleClose()}>Cancel</Button>
                <Button startIcon={<SaveIcon />} onClick={() => {
                    const newItem: { [key: string]: any } = {};
                    props.model.generateColumns().forEach(column => {
                        const inputElement = document.getElementById(column.field) as HTMLInputElement;
                        if (inputElement) {
                            newItem[column.field] = inputElement.value;
                        }
                    });
                    props.handleSave(newItem);
                }}>Save</Button>
            </DialogActions>
        </Dialog>
    )
}

// This EditToolBar is the method to add an item
function EditToolbar(props: EditToolbarProps) {
    // Set the method to read the rows and elements from the item
    const { setData, setDataModesModel, model } = props;

    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const handleSave = (newItem: GridValidRowModel) => {
        setData((oldData) => {
            const maxId = oldData.length > 0 ? Math.max(...oldData.map(row => row.id)) : 0;
            const id = maxId + 1;
            return [
                ...oldData,
                { id, ...newItem },
            ];
        });
        setOpen(false);
    };

    return (
        <>
            {/* Add the button to add an item, this would be up the table */}
            <GridToolbarContainer>
                <Button
                    color="secondary"
                    startIcon={<AddOutlinedIcon />}
                    onClick={handleClickOpen}>
                    Add item
                </Button>
            </GridToolbarContainer>
            {/* Add the dialog to add an item */}
            <ItemDialog
                open={open}
                handleClose={handleClose}
                handleSave={handleSave}
                model={model}
            />
        </>
    );
}

// Also, define the actions component. This component would help us to
// upgrade (or delete) an item

// Add the return type as a GridColDef
function EditMode(props: { data: DataTableModel[], handleSave: CallableFunction, model: DataTableModel }): GridColDef {
    const [open, setOpen] = React.useState(false);
    const [alertOpen, setAlertOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const handleDeleteClick = (id: GridRowId) => {
        const data = props.data.filter((row) => row.id !== id);
        setAlertOpen(true);
        setTimeout(() => setAlertOpen(false), 3000); // Hide alert after 3 seconds
        // Modify the data after those three seconds
        setTimeout(() => props.handleSave(data), 3000);
    };

    return {
        field: 'actions',
        type: 'actions',
        headerName: '',
        width: 100,
        cellClassName: 'actions',
        renderCell: (params) => (
            <>
                <GridActionsCellItem
                    icon={<EditIcon />}
                    label="Edit"
                    className="textPrimary"
                    onClick={handleClickOpen}
                    color="inherit"
                />
                <GridActionsCellItem
                    icon={<DeleteIcon />}
                    label="Delete"
                    onClick={() => handleDeleteClick(params.id)}
                    color="inherit"
                />
                <ItemDialog
                    open={open}
                    handleClose={handleClose}
                    handleSave={props.handleSave}
                    model={props.model}
                    data={params.row}
                />
                {alertOpen && (
                    <div style={{ position: 'fixed', bottom: 0, left: 0, width: '100%', zIndex: 9999 }}>
                        <Stack sx={{ width: '100%' }} spacing={2}>
                            <Alert severity="warning">Item was deleted successfully!</Alert>
                        </Stack>
                    </div>
                )}
            </>
        ),
    };
}

// Define the DataTable. This table it's supposed to be dynamic and easy to use, implementing data
// that can be modified from below steps and with rows that can be easily modified with an specific time.
export const DataTable: React.FC<DataTableProps> = ({
    model,
    data,
    setData,
    isEditable
}) => {
    const columns = model.generateColumns();
    // If this data is editable, then I'll add the Edit mode to the columns
    if (isEditable && setData) {
        columns.push(EditMode({ data, handleSave: setData, model }));
    }
    // Create an state for the rowModes
    const [dataModesModel, setDataModesModel] = React.useState<GridRowModesModel>({});


    // The setData is the method we use to modify the data IN CASE that we have to do so
    // (as, for example, delete an entry or modify an entry)
    return (
        <Paper sx={{ marginTop: "1em", height: 400, width: '99%' }}>
            <DataGrid
                rows={data}
                columns={columns}
                initialState={{ pagination: { paginationModel }, columns: { columnVisibilityModel: { id: false } } }}
                pageSizeOptions={[5, 10]}
                editMode='row'
                slots={{
                    toolbar: EditToolbar as GridSlots['toolbar'],
                }}
                slotProps={{
                    toolbar: { setData, setDataModesModel, model }
                }}
                sx={{
                    border: 0.1,
                    borderColor: "#666666", // This color make the border better looking
                    borderRadius: "1em"
                }}
            />
        </Paper>
    );
}

export default DataTable;