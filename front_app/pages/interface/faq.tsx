/// * FAQ Page
/// *
/// * This page include information about the problem
// ===========================
// React imports
import React from 'react';
// Include the alerts
// MUI imports
import { Box, Typography, Divider } from '@mui/material';
import ConstructionOutlinedIcon from '@mui/icons-material/ConstructionOutlined';
// Local imports
import { PageTemplate, AvailablePages, PageChildrenProps } from "../../components/PageTemplate";
import { colorTokens } from '../../theme';


const FaqPage: React.FC<PageChildrenProps> = ({ open, setOpen }) => {
    const colors = colorTokens();

    return (
        <PageTemplate
            page={AvailablePages.FAQ}
            open={open}
            setOpen={setOpen}
        >
            <Box alignItems="center" marginTop="2em">
                <Divider />
                <Typography variant="h5" margin="3em" align='center' color={colors.grey[300]}>
                    <ConstructionOutlinedIcon color="secondary" sx={{
                        fontSize: "5em"
                    }} />
                </Typography>
                <Typography variant="h4" margin="3em" align='center' color={colors.grey[300]}>
                    Page still on work, please come back later.
                </Typography>
                <Divider />
            </Box>
        </PageTemplate>
    )
}

export default FaqPage;
