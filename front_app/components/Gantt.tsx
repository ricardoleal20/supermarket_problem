/// * Gantt compoent
/// * 
/// * Gantt to show how does behave the solution around each cashier and the clients
/// * @packageDocumentation
/// * @module Gantt
import React from 'react';
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
};

interface Event {
    id: number,
    eventId: number,
    title: string,
    start: Date,
    end: Date,
    color?: string
}

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
            element.title,
            createDateTime(element.start),
            createDateTime(element.end),
        ]
        // Append the event to the events
        events.push(event);
    });
    // Return the events
    return events;
};

export default function Gantt({ data }: GanttProps) {
    // Create the events for the scheduler section
    const events = mapDataToEvents(data);
    // Define the component for the gantt
    // Add custom resources
    // const customResources = ["Resource 1", "Resource 2", "Resource 3"];
    // customResources.forEach(resource => {
    //     if (!events.some(event => event[0] === resource)) {
    //         events.push([resource, "", new Date(0, 0, 0, 7, 0, 0), new Date(0, 0, 0, 7, 0, 0)]);
    //     }
    // });

    return (
        <Chart
            chartType="Timeline"
            width="100%"
            height="400px"
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