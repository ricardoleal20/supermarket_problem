//* Section block. This is to define information around the page using a simple structure
// ==============================
import { Box } from "@mui/material";
import React from "react";
// Local imports
import { colorTokens } from "../theme";

interface TextBlockProps {
    children: React.ReactNode;
    width?: string;
    height?: string;
}

const TextBlock: React.FC<TextBlockProps> = ({
    children,
    width = "100%",
    height = "100%"
}) => {
    // Get the colors
    const colors = colorTokens();
    // Define the elements here for the text block section
    return (
        <Box
            padding="1.5em"
            justifyContent="center"
            width={width}
            height={height}
            bgcolor={colors.grey[800]}
            borderRadius="1em"
        >
            {/* Use the children here */}
            {children}
        </Box>
    )
};

export default TextBlock;
