/// * Page with a Sidebar
/// *
/// * This page contains the structure to include children and also having a sidebar
/// * This is the important thing to use in this project to show the information in the main package
/* Mui imports */
import { Box, Typography } from '@mui/material';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
// Icons import
import StoreMallDirectoryIcon from '@mui/icons-material/StoreMallDirectory';
import BorderClearIcon from '@mui/icons-material/BorderClear';
import GroupOutlinedIcon from '@mui/icons-material/GroupOutlined';
import QuizOutlinedIcon from '@mui/icons-material/QuizOutlined';
import HandymanOutlinedIcon from '@mui/icons-material/HandymanOutlined';
// Local imports
import Sidebar from "./SideBar";
import React from 'react';
import { colorTokens } from '../theme';

// Create an enum for the pages
export enum AvailablePages {
    CashierData = "Cashier Data",
    Clients = "Clients",
    RunSolver = "Generate solution",
    FAQ = "FAQ",
    NotFound = "404" // This is not going to be showed in the sidebar, but it's helpful
}

// ************************* //
// *      INTERFACES       * //
// ************************* //

interface SidebarSectionProps {
    section: string
    open: boolean
}

// Create the interface for the input of the template
interface PageTemplateProps {
    page: AvailablePages,
    // Add the open and set open props
    open: boolean,
    setOpen: CallableFunction,
    // Add the custom button header section
    customButtonHeader?: React.ReactNode
    // Add the children
    children: React.ReactNode
};

interface SideBarElementProps {
    page: AvailablePages,
    open: boolean,
    selected: string,
    refUrl: string
}

export interface PageChildrenProps {
    open: boolean
    setOpen: CallableFunction
}

// Create the Header section type
const SidebarSection: React.FC<SidebarSectionProps> = ({ section, open }) => {
    // Instance the color props
    if (open == true) {
        const colors = colorTokens();
        return (
            <Box>
                <Typography variant="h5" sx={{
                    marginLeft: "1.5em",
                    marginTop: "1em",
                    marginBottom: "0.2em",
                    color: colors.grey[300]
                }}>
                    {section}
                </Typography>
                <Divider />
            </Box>
        )
    }
    return (<Divider />)
}

function getItemIcon(text: string): React.ReactNode {
    // 
    switch (text) {
        case AvailablePages.CashierData: {
            return (<StoreMallDirectoryIcon />)
        }
        case AvailablePages.Clients: {
            return (<GroupOutlinedIcon />)
        }
        case AvailablePages.FAQ: {
            return (<QuizOutlinedIcon />)
        }
        case AvailablePages.RunSolver: {
            return (<HandymanOutlinedIcon />)
        }
        // Just in case that I forgot to add the icon or that I miss-spell
        // a case in this scenario
        default: {
            return (<BorderClearIcon />)
        }
    }
}


const SideBarElement: React.FC<SideBarElementProps> = ({ page, open, selected, refUrl }) => {
    // Create the full page with the item desired. In this case, we'll use
    // 'interface' with the desired extension

    const link = "http://localhost:5173/interface/" + refUrl

    return (
        <ListItem key={page} disablePadding sx={{ display: 'block' }}>
            <ListItemButton
                // Define if this is the selected page or not
                selected={selected === page}
                // disabled={selected === page} // If the page is selected, we cannot re-selected
                href={link}
                sx={[
                    {
                        minHeight: 48,
                        px: 2.5,
                    },
                    open
                        ? {
                            justifyContent: 'initial',
                        }
                        : {
                            justifyContent: 'center',
                        },
                ]}
            >
                <ListItemIcon
                    sx={[
                        {
                            minWidth: 0,
                            justifyContent: 'center',
                        },
                        open
                            ? {
                                mr: 3,
                            }
                            : {
                                mr: 'auto',
                            },
                    ]}
                >
                    {getItemIcon(page)}
                </ListItemIcon>
                <ListItemText
                    primary={page}
                    sx={[
                        open
                            ? {
                                opacity: 1,
                            }
                            : {
                                opacity: 0,
                            },
                    ]}
                />
            </ListItemButton>
        </ListItem >
    )
};

// Select the possible elements for the drawer
const SidebarElements = (open: boolean, selectedPage: string) => {
    return (
        <List>
            {/* Add the elements one by one */}
            {open && <SidebarSection section="Data" open={open} />}
            <SideBarElement page={AvailablePages.CashierData} open={open} selected={selectedPage} refUrl='cashier_data' />
            <SideBarElement page={AvailablePages.Clients} open={open} selected={selectedPage} refUrl='clients' />

            <SidebarSection section="Solution" open={open} />
            <SideBarElement page={AvailablePages.RunSolver} open={open} selected={selectedPage} refUrl='run' />
            {/* Add the Extra info section*/}
            <SidebarSection section="" open={open} />
            <SideBarElement page={AvailablePages.FAQ} open={open} selected={selectedPage} refUrl='FAQ' />


        </List>
    )
}


export const PageTemplate: React.FC<PageTemplateProps> = ({
    page,
    children,
    open,
    setOpen,
    customButtonHeader = null
}) => {
    return (
        // Start the sidebar
        <Sidebar
            headerTitle={page}
            selected={page}
            sidebarElements={SidebarElements}
            open={open}
            setOpen={setOpen}
            customButtonHeader={customButtonHeader}
        >
            {children}
        </Sidebar>
    )
};

