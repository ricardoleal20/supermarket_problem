// * UTILITIES FOR THE ENTIRE PROEJCT */


interface ColoredLineProps {
  color: string;
  width?: string;
  marginBottom?: string;
  marginTop?: string,
}


// Define a colored line to be added in the pages or sidebar
export const ColoredLine: React.FC<ColoredLineProps> = ({
  color, width = "100%",
  marginTop = "0",
  marginBottom = "0",
}) => (
  <hr
    style={{
      color: color,
      backgroundColor: color,
      height: 0.5,
      width: width,
      marginBottom: marginBottom,
      marginTop: marginTop,
    }}
  />
);

// Create a method to perform a request to an API
export const performRequest = async (endpoint: string, method: string, body: any) => {
  const url = "http://localhost:3000/" + endpoint;
  // Perform the request
  const response = await fetch(url, {
    method: method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  // Get the data
  const data = await response.json();
  return data;
};