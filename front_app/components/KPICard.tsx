/// * KPI Card info
/// * 
/// * KPI card information. It includes the optioon to add a title
/// * and a value. It also includes the option to add a custom icon
/// * @packageDocumentation
/// * @module KPICard

import React from 'react';
import { Box, Typography, Divider, Card } from '@mui/material';

interface KPICardProps {
    title: string;
    value: string | number;
    description: string;
    icon?: React.ReactNode;
};

export default function KPICard({ title, value, icon, description }: KPICardProps) {
    return (
        <Card variant="outlined" sx={{
            borderRadius: "1em",
            maxWidth: "22%",
            transition: "all 0.3s ease-in-out",
            '&:hover': {
                maxWidth: "25%",
                borderColor: "secondary.main",
                // boxShadow: 3,
            }
        }}>
            <Box p={2}>
                <Typography variant="h4" color="textSecondary">
                    {icon} {title}
                </Typography>
                <Divider />
                <Box display="flex" justifyContent="space-around" marginTop="0.5em">
                    <Typography variant="h1">
                        {value}
                    </Typography>
                    <Divider orientation="vertical" flexItem />
                    <Typography variant="h6" color="secondary.contrastText" sx={{ maxWidth: "70%", fontSize: "" }}>
                        {description}
                    </Typography>
                </Box>
            </Box>
        </Card>
    );
};