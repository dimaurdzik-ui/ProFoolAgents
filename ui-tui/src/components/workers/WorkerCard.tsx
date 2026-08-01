import { Box, Text } from '@pixel-agents/ink';
import React from 'react';

export interface WorkerCardProps {
    workerId: string;
    displayName: string;
    status: string;
    autonomyMode: string;
    isSelected?: boolean;
}

export function WorkerCard({ workerId, displayName, status, autonomyMode, isSelected }: WorkerCardProps) {
    return (
        <Box borderColor={isSelected ? 'green' : 'gray'} borderStyle="round" flexDirection="column" paddingX={1}>
            <Box>
                <Text bold color={isSelected ? 'green' : 'white'}>{displayName}</Text>
                <Text dimColor> ({workerId})</Text>
            </Box>
            <Box marginTop={1}>
                <Text color="cyan">Status: {status}</Text>
                <Text dimColor> | Mode: {autonomyMode}</Text>
            </Box>
        </Box>
    );
}
