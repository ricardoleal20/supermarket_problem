/// * Scatter component
/// * 
/// * This component is used to display a scatter chart with the data provided.
/// * It would be: Arrival Time to the Queue vs Start processing time
import { ScatterChart } from '@mui/x-charts/ScatterChart';


interface InnerData {
    id: string
    x: number
    y: number
}

export interface ScatterData {
    label: string,
    data: InnerData[]
}

interface ScatterProps {
    data: ScatterData[];
    width?: number;
    height?: number;
}

function axisFormated(value: number) {
    // Depenging on the value, we'll show the hour
    const hour = Math.floor(value / 60) + 8;
    const minute = value % 60;

    const minuteStr = minute < 10 ? `0${minute}` : `${minute}`;
    // Now, if the hour is less than 6, then we'll show it as it is
    // plus the P.M. suffix
    return `${hour}:${minuteStr}`;
    // if (hour < 6) {
    //     return `${hour + 8}:${minuteStr} A.M.`;
    // } else {
    //     return `${hour}:${minuteStr} P.M.`;
    // }
}

export function ScatterGant({ data, width, height }: ScatterProps) {
    return (
        <ScatterChart
            title="Arrival Time to the Queue vs Start processing time"
            xAxis={[{
                label: "Arrival Time to the Queue",
                valueFormatter: (value) => {
                    return axisFormated(value);
                }
            }]}
            yAxis={[{
                // label: "Start processing time",
                valueFormatter: (value) => {
                    return axisFormated(value);
                }
            }]}
            series={data}
            width={width ?? 500}
            height={height ?? 300}
            slotProps={{ legend: { hidden: true } }}
        />
    )
};