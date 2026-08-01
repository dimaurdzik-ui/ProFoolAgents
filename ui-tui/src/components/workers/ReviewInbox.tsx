import { Box, Text } from '@pixel-agents/ink';
import React from 'react';

export interface Task {
    id: string;
    goal: string;
    worker_id: string;
    worker_role?: string;
    worker_name?: string;
    status: string;
    created_at: number;
    result?: string;
}

export interface ReviewInboxProps {
    tasks: Task[];
    onApprove: (taskId: string) => void;
    onReject: (taskId: string, feedback: string) => void;
    selectedIndex?: number;
}

export function ReviewInbox({ tasks, selectedIndex = 0 }: ReviewInboxProps) {
    const pendingTasks = tasks.filter(t => t.status === 'waiting_approval');

    if (pendingTasks.length === 0) {
        return (
            <Box borderStyle="round" padding={1}>
                <Text color="gray">No tasks waiting for review in the inbox.</Text>
            </Box>
        );
    }

    return (
        <Box borderStyle="round" flexDirection="column" padding={1}>
            <Text bold color="yellow" marginBottom={1}>Inbox: {pendingTasks.length} Tasks Require Approval</Text>
            {pendingTasks.map((task, index) => (
                <Box flexDirection="column" key={task.id} marginBottom={1} paddingLeft={1}>
                    <Text bold color={index === selectedIndex ? 'green' : undefined}>{index === selectedIndex ? '› ' : '  '}Task: {task.goal}</Text>
                    <Text color="blue">Worker: {task.worker_name ?? task.worker_id}{task.worker_role ? ` (${task.worker_role})` : ''}</Text>
                    <Text color="gray">ID: {task.id}</Text>
                    {task.result ? <Text wrap="truncate-end">Result: {task.result}</Text> : null}
                    {index === selectedIndex ? <Text color="magenta">y approve · n reject with feedback</Text> : null}
                </Box>
            ))}
        </Box>
    );
}
