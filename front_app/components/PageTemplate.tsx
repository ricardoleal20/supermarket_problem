/// * Page with a Sidebar
/// *
/// * This page contains the structure to include children and also having a sidebar
/// * This is the important thing to use in this project to show the information in the main package
/* Mui imports */
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
// Icons import
import StoreMallDirectoryIcon from '@mui/icons-material/StoreMallDirectory';
import BorderClearIcon from '@mui/icons-material/BorderClear';
// Local imports
import Sidebar from "./SideBar";
import React from 'react';

// Create an enum for the pages
export enum AvailablePages {
    CashierData = "Cashier Data"
}

// Create the interface for the input of the template
interface PageTemplateProps {
    page: AvailablePages,
    children: React.ReactNode
};

function getItemIcon(text: string): React.ReactNode {
    // 
    switch (text) {
        case "Cashier Data": {
            return (
                <StoreMallDirectoryIcon />
            )
        }
        // Just in case that I forgot to add the icon or that I miss-spell
        // a case in this scenario
        default: {
            return (
                <BorderClearIcon />
            )
        }
    }
}

interface SideBarElementProps {
    page: AvailablePages,
    open: boolean,
    selected: string
}

const SideBarElement: React.FC<SideBarElementProps> = ({ page, open, selected }) => {
    return (
        <ListItem key={page} disablePadding sx={{ display: 'block' }}>
            <ListItemButton
                // Define if this is the selected page or not
                selected={selected === page}
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
            {/* Add the elemtns one by one */}
            <SideBarElement page={AvailablePages.CashierData} open={open} selected={selectedPage} />
        </List>
    )
}


export const PageTemplate: React.FC<PageTemplateProps> = ({
    page,
    children
}) => {
    return (
        // Start the sidebar
        <Sidebar
            headerTitle={page}
            selected={page}
            sidebarElements={SidebarElements}
        >
            {children}
        </Sidebar>
    )
};

