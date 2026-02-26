import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Button,
  LinearProgress,
  Chip,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Description as FileIcon,
  Folder as FolderIcon,
  Delete as DeleteIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';

interface FileItem {
  id: string;
  name: string;
  type: 'file' | 'folder';
  size: number;
  createdAt: string;
  path: string;
}

const FileManager: React.FC = () => {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      setLoading(true);
      // Mock data - replace with actual API call
      setFiles([
        {
          id: '1',
          name: 'Business Report.pdf',
          type: 'file',
          size: 1024000,
          createdAt: '2024-01-15T10:30:00Z',
          path: '/documents/Business Report.pdf',
        },
        {
          id: '2',
          name: 'Research Data',
          type: 'folder',
          size: 0,
          createdAt: '2024-01-15T09:15:00Z',
          path: '/documents/Research Data',
        },
        {
          id: '3',
          name: 'Technical Documentation.docx',
          type: 'file',
          size: 512000,
          createdAt: '2024-01-15T08:45:00Z',
          path: '/documents/Technical Documentation.docx',
        },
        {
          id: '4',
          name: 'Meeting Notes.txt',
          type: 'file',
          size: 10240,
          createdAt: '2024-01-15T07:30:00Z',
          path: '/documents/Meeting Notes.txt',
        },
      ]);
    } catch (error) {
      console.error('Failed to fetch files:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      uploadFile(file);
    }
  };

  const uploadFile = async (file: File) => {
    try {
      setUploading(true);
      // Mock upload - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const newFile: FileItem = {
        id: Date.now().toString(),
        name: file.name,
        type: 'file',
        size: file.size,
        createdAt: new Date().toISOString(),
        path: `/documents/${file.name}`,
      };
      
      setFiles([newFile, ...files]);
    } catch (error) {
      console.error('Failed to upload file:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = (fileId: string) => {
    console.log('Download file:', fileId);
    // Download logic
  };

  const handleDelete = (fileId: string) => {
    console.log('Delete file:', fileId);
    setFiles(files.filter(f => f.id !== fileId));
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  if (loading) {
    return <LinearProgress />;
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          File Manager
        </Typography>
        <Button
          variant="contained"
          component="label"
          startIcon={<UploadIcon />}
          disabled={uploading}
        >
          Upload File
          <input
            type="file"
            hidden
            onChange={handleFileUpload}
          />
        </Button>
      </Box>

      {uploading && (
        <Box sx={{ mb: 2 }}>
          <LinearProgress />
          <Typography variant="body2" color="textSecondary">
            Uploading file...
          </Typography>
        </Box>
      )}

      <Paper>
        <List>
          {files.map((file) => (
            <ListItem
              key={file.id}
              divider
              secondaryAction={
                <Box>
                  <IconButton
                    edge="end"
                    onClick={() => handleDownload(file.id)}
                    disabled={file.type === 'folder'}
                  >
                    <DownloadIcon />
                  </IconButton>
                  <IconButton
                    edge="end"
                    onClick={() => handleDelete(file.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Box>
              }
            >
              <ListItemIcon>
                {file.type === 'folder' ? <FolderIcon /> : <FileIcon />}
              </ListItemIcon>
              <ListItemText
                primary={file.name}
                secondary={
                  <Box>
                    <Typography variant="caption" display="block">
                      {file.path}
                    </Typography>
                    <Box display="flex" alignItems="center" gap={1}>
                      {file.type === 'file' && (
                        <Chip
                          label={formatFileSize(file.size)}
                          size="small"
                          variant="outlined"
                        />
                      )}
                      <Chip
                        label={file.type.toUpperCase()}
                        size="small"
                        color={file.type === 'folder' ? 'primary' : 'default'}
                      />
                      <Typography variant="caption" color="textSecondary">
                        {new Date(file.createdAt).toLocaleDateString()}
                      </Typography>
                    </Box>
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
      </Paper>

      {files.length === 0 && (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="h6" color="textSecondary">
            No files found
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Upload some files to get started
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default FileManager;
