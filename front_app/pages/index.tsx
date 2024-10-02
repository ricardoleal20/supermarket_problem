/// Index Page. This is the page that would redirect it to the others
/// `project` page.
import { Box, Typography } from "@mui/material";
// Local imports
import "../animated_background.css";

const Home = () => {
    return (
        <Box
            className="index_class"
            textAlign="center"
            justifyContent="space-between"
            height="100%" // Give the height neccesary to be shown in the page
            width="100%" // Just give the 100% to ensure the entire X length to be used in the animation
        >
            {/* Define the box for the information section */}
            <Box paddingTop="8em" justifyContent="space-between">
                <Typography variant="h1">Optimized Flexible Supermarket Solution</Typography>
                {/* Define the container */}
            </Box>
        </Box>
    );
}

export default Home;