/// * Pie Chart
/// *
/// * Pie chart component that displays the data in a pie chart format. This would
/// * be used to display the general efficiency of the cashiers in both shifts.
/// * This efficiency would be taking in consideration the service level, the 
/// * average queue waiting time, the average processing time and the average free
/// * time of the cashiers. 

import { PieChart, pieArcLabelClasses } from '@mui/x-charts/PieChart';

export interface EfficiencyData {
    id: number,
    value: number,
    label: string
}

interface PieChartProps {
    data: EfficiencyData[];
    width?: number;
    height?: number;
}

export function PieChartComponent({ data, width, height }: PieChartProps) {
    return (
        <PieChart
            series={[{
                data: data,
                highlightScope: { fade: 'global', highlight: 'item' },
                faded: { innerRadius: 30, additionalRadius: -30, color: 'gray' },
                // arcLabel: (item) => `${item.label}: ${item.value}%`,
                valueFormatter: (item) => `${item.value}%`,
                arcLabelMinAngle: 35,
                arcLabelRadius: '60%',
                // innerRadius: 30
                // outerRadius: 60
            },
                // {
                //     data: data,
                //     highlightScope: { fade: 'global', highlight: 'item' },
                //     faded: { innerRadius: 30, additionalRadius: -30, color: 'gray' },
                //     // arcLabel: (item) => `${item.label}: ${item.value}%`,
                //     valueFormatter: (item) => `${item.value}%`,
                //     arcLabelMinAngle: 35,
                //     arcLabelRadius: '60%',
                //     innerRadius: 70
                // }
            ]}
            sx={{
                [`& .${pieArcLabelClasses.root}`]: {
                    fontWeight: 'bold',
                },
            }}
            width={width ?? 300}
            height={height ?? 200}
            slotProps={{ legend: { hidden: true } }}
        />
    )
}