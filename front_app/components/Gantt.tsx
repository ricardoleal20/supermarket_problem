/// * Gantt compoent
/// * 
/// * Gantt to show how does behave the solution around each cashier and the clients
/// * @packageDocumentation
/// * @module Gantt
// Imports for the Gantt chart
import { Chart } from "react-google-charts";


const Fields = [
    { type: "string", id: "Processor" },
    { type: "string", id: "Task" },
    { type: "number", id: "Start" },
    { type: "number", id: "End" },
]
// Defien the interface for the Gantt component
interface GanttProps {
    data: any;
    allResources?: string[];
    width?: number;
    height?: number;
};

// Let's create a function to map the data to events
// and return the events
const mapDataToEvents = (data: any): any[] => {
    // Define the events
    const events: any[] = [Fields];
    // Iterate over the data
    data.forEach((element: any) => {
        // Define the event
        const createDateTime = (arrivalTime: number): Date => {
            // Get the base hour
            const baseHour = 8;
            const hour = baseHour + Math.floor(arrivalTime / 60);
            const minutes = arrivalTime % 60;
            // Return the date at the end
            return new Date(0, 0, 0, hour, minutes, 0);
        };

        // const event = {
        //     id: element.id,
        //     eventId: element.id,
        //     title: element.title,
        //     start: createDateTime(element.start),
        //     end: createDateTime(element.end),
        // };
        const event = [
            element.processor,
            "",
            createDateTime(element.start),
            createDateTime(element.end),
        ]
        // Append the event to the events
        events.push(event);
    });
    // Return the events
    return events;
};

export default function Gantt({ data, allResources, width, height }: GanttProps) {
    // Create the events for the scheduler section
    const events = mapDataToEvents(data);
    // Define the component for the gantt
    // Add custom resources
    if (allResources) {
        allResources.forEach(resource => {
            if (!events.some(event => event[0] === resource)) {
                events.push([resource, "", new Date(0, 0, 0, 8, 0, 0), new Date(0, 0, 0, 8, 0, 0)]);
            }
        });

        // Sort the events by their resource (first column)
        // events.sort((a, b) => {
        //     if (a[0] < b[0]) return -1;
        //     if (a[0] > b[0]) return 1;
        //     return 0;
        // });
    }

    return (
        <Chart
            chartType="Timeline"
            width={width ?? "100%"}
            height={height ?? "300px"}
            data={events}
            options={{
                timeline: {
                    showRowLabels: true,
                    showBarLabels: false,
                    colorByRowLabel: true,
                    rowLabelStyle: {
                        fontSize: 15, // Adjust the font size if needed
                        // height: 500, // Set the custom height for each row
                    },
                    barLabelStyle: {
                        fontSize: 25,
                    }
                    // singleColor: '#8d8',
                },
                hAxis: {
                    minValue: new Date(0, 0, 0, 8, 0, 0),
                    maxValue: new Date(0, 0, 0, 20, 0, 0),
                    title: 'Time', // Add a title to the x-axis
                    textStyle: {
                        color: "#ffffff" // Set the text color to white
                    }
                },
            }}
        />
    )
}