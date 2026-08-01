import { Box, Text } from '@pixel-agents/ink';
import React from 'react';

export interface WorkerOnboardingDialogProps {
    templateId: string;
    onConfirm: (displayName: string) => void;
    onCancel: () => void;
}

export function WorkerOnboardingDialog({ templateId }: WorkerOnboardingDialogProps) {
    // A placeholder for a real interactive dialog using ink-text-input or similar
    return (
        <Box borderColor="yellow" borderStyle="round" flexDirection="column" padding={1}>
            <Text bold color="yellow">Hire New Worker ({templateId})</Text>
            <Box marginTop={1}>
                <Text>Please enter a display name for this worker and press Enter.</Text>
            </Box>
            <Box marginTop={1}>
                <Text dimColor>[Interactive prompt would appear here]</Text>
            </Box>
        </Box>
    );
}
