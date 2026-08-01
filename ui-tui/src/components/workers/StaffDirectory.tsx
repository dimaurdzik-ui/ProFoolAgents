import { Box, Text } from '@pixel-agents/ink';
import React from 'react';

import { WorkerCard } from './WorkerCard.js';

export interface Worker {
    worker_id: string;
    template_id: string;
    display_name: string;
    status: string;
    autonomy_mode: string;
    manager_id?: string;
    created_at: number;
}

export interface StaffDirectoryProps {
    workers: Worker[];
    selectedIndex: number;
}

export function StaffDirectory({ workers, selectedIndex }: StaffDirectoryProps) {
    if (workers.length === 0) {
        return (
            <Box borderStyle="round" flexDirection="column" padding={1}>
                <Text bold color="cyan">Staff Directory</Text>
                <Text color="gray" marginTop={1}>No workers hired yet. Use `workers.hire` to onboard a new digital employee.</Text>
            </Box>
        );
    }

    return (
        <Box borderStyle="round" flexDirection="column" padding={1} width="100%">
            <Text bold color="cyan" marginBottom={1}>Staff Directory ({workers.length} Total)</Text>
            <Box flexDirection="column" gap={1}>
                {workers.map((worker, index) => (
                    <Box key={worker.worker_id} width="100%">
                        <WorkerCard 
                            autonomyMode={worker.autonomy_mode}
                            displayName={worker.display_name}
                            isSelected={index === selectedIndex}
                            status={worker.status}
                            workerId={worker.worker_id}
                        />
                    </Box>
                ))}
            </Box>
        </Box>
    );
}
