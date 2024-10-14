// MUI imports
import React, { useEffect, useState } from 'react';
import {
    DataGrid, GridColDef, GridRowsProp, GridRowModesModel,
    GridToolbarContainer, GridSlots, GridActionsCellItem,
    GridValidRowModel,
    GridRowId
} from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import { DialogContent, DialogActions, Dialog, TextField, Typography, Box } from '@mui/material';
// Include the alert imports
import Stack from '@mui/material/Stack';
import Alert from '@mui/material/Alert';
// Import icons
import AddOutlinedIcon from '@mui/icons-material/Add'
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
// Local imports
import { colorTokens } from '../theme';

const paginationModel = { page: 0, pageSize: 5 };

// ****************** //
// Interfaces

interface HashSet<T = any> {
    [key: string]: T; // With this, i know that the entries are going to be string but the response can be anything!
}

export type FieldsInfo = HashSet | GridColDef;


export interface DataTableModel {
    id: GridRowId;
    getFieldsInfo: () => GridColDef[];
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

function ItemDialog(
    props: {
        open: boolean,
        handleClose: CallableFunction,
        handleSave: CallableFunction,
        model: DataTableModel,
        data?: HashSet
    }
) {
    const colors = colorTokens();
    // Create a local state to store the form values
    const [formValues, setFormValues] = useState<{ [key: string]: any }>({});

    // When the dialog gets open, we'll initialize the state with the data provided (if it exists)
    useEffect(() => {
        if (props.data) {
            setFormValues(props.data);
        } else {
            // Si no hay datos, inicializa el estado con campos vacíos
            const initialValues: { [key: string]: any } = {};
            props.model.getFieldsInfo().forEach(column => {
                initialValues[column.field] = '';  // Initial value of each field
            });
            setFormValues(initialValues);
        }
    }, [props.data, props.model]);

    // Function to manage the input change for each one of the fields
    const handleInputChange = (field: string, value: any) => {
        setFormValues(prevValues => ({
            ...prevValues,
            [field]: value
        }));
    };

    return (
        <Dialog open={props.open} onClose={() => props.handleClose()}>
            {/* Define a box to show the dialog title and an icon */}
            <Box sx={{ marginTop: "1.5em", marginLeft: "1.5em", }}>
                <Typography variant="h2" sx={{ color: colors.primary[100] }}>
                    <Box display="flex" alignItems="center">
                        <Box alignItems="center" sx={{ borderRadius: "50%", backgroundColor: colors.greenAccent[800], marginRight: "0.3em" }}>
                            <EditOutlinedIcon
                                fontSize="large"
                                style={{
                                    marginRight: "0.25em",
                                    marginLeft: "0.25em",
                                    marginTop: "0.25em",
                                    marginBottom: "0.25em",
                                    color: colors.greenAccent[500]
                                }} />
                        </Box>
                        <Box display="flex" flexDirection="column">
                            <Typography variant="h3">Add Item</Typography>
                            <Typography variant="h5" sx={{ color: colors.grey[300] }}>Include item information</Typography>
                        </Box>
                    </Box>
                </Typography>
            </Box>

            <DialogContent sx={{ minWidth: "40em", backgroundColor: colors.primary[500] }}>

                {/* Automatically render the fields based on the model columns */}
                {props.model.getFieldsInfo()
                    .filter((column) => column.field !== 'id')
                    .map((column) => (
                        <div key={column.field}>
                            <Typography variant="h5" marginTop="0.5em">
                                {column.labelIcon ? column.labelIcon() : null}
                                {column.headerName || column.field.charAt(0).toUpperCase() + column.field.slice(1)}
                            </Typography>
                            <TextField
                                margin="dense"
                                color="secondary"
                                id={column.field}
                                type={column.type || "text"}
                                placeholder={column.headerName || column.field.charAt(0).toUpperCase() + column.field.slice(1)}
                                fullWidth
                                variant="outlined"
                                value={formValues[column.field] || ''}
                                onChange={(e) => handleInputChange(column.field, e.target.value)}
                                sx={{
                                    '& .MuiFilledInput-root': {
                                        borderRadius: '50%',
                                    },
                                }}
                            />
                        </div>
                    ))}
            </DialogContent>
            <DialogActions sx={{ backgroundColor: colors.primary[500] }}>
                {/* Botons to decide the action to consider for the dialog */}
                <Button startIcon={<CancelIcon />} sx={{
                    border: 0, borderRadius: 1, backgroundColor: colors.grey[800], color: colors.primary[100]
                }} onClick={() => props.handleClose()}>Cancel</Button>
                <Button startIcon={<SaveIcon />} sx={{
                    border: 0, borderRadius: 1, backgroundColor: colors.greenAccent[700], color: colors.primary[800]
                }} onClick={() => {
                    console.log("Save the item", formValues);
                    props.handleSave(formValues);  // Pass the sate to the handleSave method
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

    // Create the save method for the delete click method
    const saveEditMethod = (newData: HashSet) => {
        // Find the index of the model that we're going to modify
        const index = props.data.findIndex((row) => row.id === newData.id);
        console.log("Index: ", index, newData.id, props.data[0].id, newData);
        if (index !== -1) {
            console.log("Mmmm apoco si?");
            // Create a copy of the data array
            const updatedData = [...props.data];
            // Replace the old data with the new data at the found index
            updatedData[index] = {
                ...updatedData[index],
                ...newData
            };
            // Update the data internally, replacing the original data model
            props.handleSave(updatedData);
        }
        // Also, close the dialog
        handleClose();
    }

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
                    handleSave={saveEditMethod}
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
    const columns = model.getFieldsInfo();
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