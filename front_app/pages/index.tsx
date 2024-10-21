/// Index Page. This is the page that would redirect it to the others
/// `project` page.
import { Box, Typography, Button, Link } from "@mui/material";
// Icon imports
import LaunchIcon from '@mui/icons-material/Launch';
// Local imports
import TextBlock from "../components/TextBlock";
import "../animated_background.css";
import { colorTokens } from "../theme";

const Home = () => {
    // Define the colors
    const colors = colorTokens();
    return (
        <Box
            className="index_class"
            textAlign="center"
            justifyContent="space-between"
            height="100%" // Give the height neccesary to be shown in the page
            width="100%" // Just give the 100% to ensure the entire X length to be used in the animation
        >
            {/* Define the box for the information section */}
            <Box paddingTop="8em" justifyContent="space-between" align="center">
                <Typography variant="h1" paddingBottom="0.5em">Optimized Flexible Supermarket Solution</Typography>
                {/* Define the container */}
                <TextBlock width="80%">
                    <Typography variant="h4" textAlign="left" paddingLeft="1em" paddingRight="1em">
                        This project aims to see the optimization of a supermarket by managing various aspects
                        like the cashier efficiency, their availability for working throught the day and the
                        KPIs of clients attended. Those KPIs would evaluate our setup to see how efficient it
                        is. The evaluation of this KPIs can be done employing mathematical algorithms that
                        globally searchs for a solution that can minimize costs and improve the efficiency
                        of the current setup.
                    </Typography>
                    <Typography variant="h4" paddingTop="2em">
                        For more detailed information about this solution, check
                        the <Link
                            color={colors.greenAccent[500]}
                            underline="hover"
                            sx={{
                                cursor: "pointer"
                            }}
                        >FAQ</Link> section
                        in the project.
                    </Typography>
                </TextBlock>
                {/* Add the button that redirect us to the FAQ page*/}
                <Button
                    variant="contained"
                    href="/interface"
                    size="large"
                    startIcon={<LaunchIcon />}
                    sx={{
                        marginTop: "1.5em",
                        borderRadius: "1em",
                        border: "1px solid",
                        borderColor: colors.greenAccent[500],
                        transition: "all 0.15s ease-out allow-discrete",
                        "&:hover": {
                            "background": colors.greenAccent[900]
                        }
                    }}
                >
                    Go to the project site
                </Button>
            </Box>
        </Box>
    );
}

export default Home;