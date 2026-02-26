import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  IconButton,
  LinearProgress,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Visibility as ViewIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';

interface Task {
  id: string;
  title: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  createdAt: string;
  updatedAt: string;
  progress?: number;
}

const TaskManager: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      // Mock data - replace with actual API call
      setTasks([
        {
          id: '1',
          title: 'Generate Business Report',
          status: 'completed',
          createdAt: '2024-01-15T10:30:00Z',
          updatedAt: '2024-01-15T11:45:00Z',
          progress: 100,
        },
        {
          id: '2',
          title: 'Research Market Analysis',
          status: 'running',
          createdAt: '2024-01-15T09:15:00Z',
          updatedAt: '2024-01-15T10:30:00Z',
          progress: 65,
        },
        {
          id: '3',
          title: 'Create Technical Documentation',
          status: 'pending',
          createdAt: '2024-01-15T08:45:00Z',
          updatedAt: '2024-01-15T08:45:00Z',
          progress: 0,
        },
        {
          id: '4',
          title: 'Generate User Manual',
          status: 'failed',
          createdAt: '2024-01-15T07:30:00Z',
          updatedAt: '2024-01-15T08:00:00Z',
          progress: 25,
        },
      ]);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'running':
        return 'warning';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  const handleRefresh = () => {
    fetchTasks();
  };

  const handleView = (taskId: string) => {
    console.log('View task:', taskId);
    // Navigate to task details
  };

  const handleDelete = (taskId: string) => {
    console.log('Delete task:', taskId);
    // Delete task logic
  };

  if (loading) {
    return <LinearProgress />;
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          Task Manager
        </Typography>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={handleRefresh}
        >
          Refresh
        </Button>
      </Box>

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Title</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Progress</TableCell>
                <TableCell>Created</TableCell>
                <TableCell>Updated</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {tasks.map((task) => (
                <TableRow key={task.id}>
                  <TableCell>{task.title}</TableCell>
                  <TableCell>
                    <Chip
                      label={task.status.toUpperCase()}
                      color={getStatusColor(task.status) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Box sx={{ width: '100%' }}>
                      <LinearProgress
                        variant="determinate"
                        value={task.progress || 0}
                        sx={{ mb: 1 }}
                      />
                      <Typography variant="caption">
                        {task.progress || 0}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    {new Date(task.createdAt).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    {new Date(task.updatedAt).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => handleView(task.id)}
                    >
                      <ViewIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleDelete(task.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {tasks.length === 0 && (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="h6" color="textSecondary">
            No tasks found
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Create a new document to get started
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default TaskManager;
