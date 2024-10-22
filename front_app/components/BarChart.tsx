/// * Bar Chart component
/// * 
/// * This component is used to display a bar chart with the data provided.
import { BarChart } from '@mui/x-charts/BarChart';

export interface BarChartData {
    data: number[];
    dataKey: string;
    label: string;
}

interface BarChartProps {
    data: BarChartData[];
    width?: number;
    height?: number;
}

export function BarChartByClients({ data, width, height }: BarChartProps) {
    return (
        <BarChart
            xAxis={[{
                scaleType: 'band',
                data: ['<15 products', ' 15 - 30 products', '>30 products'],
                label: 'Clients per products',
                // categoryGapRatio: 0.3,
                // barGapRatio: 0.1
            }]}
            yAxis={[{
                label: "Avg duration (minutes)"
            }]}
            series={data}
            width={width ?? 500}
            height={height ?? 300}
            slotProps={{ legend: { hidden: true } }}
            borderRadius={10}
            barLabel="value"
        />
    );
}
