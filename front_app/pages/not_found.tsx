// Get and pre-generate a not found page
// MaterialUI imports
import { Box, Typography } from "@mui/material";
// Local imports
import { ColoredLine } from "../utils";
import sadCat from "../assets/sad_cat.gif";
import { colorTokens } from "../theme";

const NotFound = () => {
    // Obtain colors
    const colors = colorTokens();
    // Set the name of the page
    // PageTitle("404");
    // We'll leave a NotFound message in the middle of the page
    return (
        <Box component="section" justifyContent="space-between" textAlign="center">
            <Typography variant="h1" marginBottom="0.5em">404</Typography>
            <img width="10%" height="10%" src={sadCat} alt="Sad Cat..." />
            {/* Write the message here */}
            <ColoredLine color={colors.grey[300]} width="30%" marginTop="1em" marginBottom="0.5em" />
            <Typography variant="h5">Page not found. Please use one of the sections.</Typography>
        </Box>
    );
};

export default NotFound;
