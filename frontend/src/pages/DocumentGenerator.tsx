import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  LinearProgress,
  Alert,
} from '@mui/material';
import {
  Description as DocumentIcon,
  Send as SendIcon,
} from '@mui/icons-material';

interface DocumentRequest {
  title: string;
  type: string;
  content: string;
  model: string;
}

const documentTypes = [
  'Business Report',
  'Research Paper',
  'Technical Documentation',
  'Proposal',
  'Meeting Minutes',
  'User Manual',
];

const models = [
  'llama3.2',
  'mistral',
  'codellama',
];

const DocumentGenerator: React.FC = () => {
  const [documentRequest, setDocumentRequest] = useState<DocumentRequest>({
    title: '',
    type: 'Business Report',
    content: '',
    model: 'llama3.2',
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleInputChange = (field: keyof DocumentRequest) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setDocumentRequest({
      ...documentRequest,
      [field]: event.target.value,
    });
  };

  const handleSubmit = async () => {
    if (!documentRequest.title || !documentRequest.content) {
      setError('Please fill in all required fields');
      return;
    }

    try {
      setLoading(true);
      setError('');
      setResult('');

      // Mock API call - replace with actual API
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setResult(`Document "${documentRequest.title}" has been generated successfully!
      
Type: ${documentRequest.type}
Model: ${documentRequest.model}

Generated content would appear here. This is a mock response since the backend API integration needs to be implemented.

The document would include:
- Executive summary
- Main content sections
- Conclusion
- References (if applicable)

Generated using ${documentRequest.model} model.`);

    } catch (err) {
      setError('Failed to generate document. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Document Generator
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Create New Document
            </Typography>
            
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Document Title"
                  value={documentRequest.title}
                  onChange={handleInputChange('title')}
                  margin="normal"
                  required
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel>Document Type</InputLabel>
                  <Select
                    value={documentRequest.type}
                    onChange={(e) => setDocumentRequest({
                      ...documentRequest,
                      type: e.target.value
                    })}
                  >
                    {documentTypes.map((type) => (
                      <MenuItem key={type} value={type}>
                        {type}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel>AI Model</InputLabel>
                  <Select
                    value={documentRequest.model}
                    onChange={(e) => setDocumentRequest({
                      ...documentRequest,
                      model: e.target.value
                    })}
                  >
                    {models.map((model) => (
                      <MenuItem key={model} value={model}>
                        {model}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>

            <TextField
              fullWidth
              label="Document Description / Requirements"
              value={documentRequest.content}
              onChange={handleInputChange('content')}
              margin="normal"
              multiline
              rows={6}
              required
              helperText="Describe what kind of document you want to generate"
            />

            <Box sx={{ mt: 2 }}>
              <Button
                variant="contained"
                startIcon={<SendIcon />}
                onClick={handleSubmit}
                disabled={loading}
                size="large"
              >
                {loading ? 'Generating...' : 'Generate Document'}
              </Button>
            </Box>

            {loading && (
              <Box sx={{ mt: 2 }}>
                <LinearProgress />
                <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                  AI is generating your document...
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Quick Templates
            </Typography>
            <Box display="flex" flexDirection="column" gap={1}>
              {documentTypes.map((type) => (
                <Chip
                  key={type}
                  label={type}
                  variant="outlined"
                  onClick={() => setDocumentRequest({
                    ...documentRequest,
                    type: type
                  })}
                  sx={{ justifyContent: 'flex-start' }}
                />
              ))}
            </Box>
          </Paper>

          <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              Tips
            </Typography>
            <Typography variant="body2" color="textSecondary">
              • Be specific about your requirements
            </Typography>
            <Typography variant="body2" color="textSecondary">
              • Include desired sections or structure
            </Typography>
            <Typography variant="body2" color="textSecondary">
              • Mention target audience
            </Typography>
            <Typography variant="body2" color="textSecondary">
              • Specify tone and style preferences
            </Typography>
          </Paper>
        </Grid>

        {result && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Generated Document
              </Typography>
              <Box
                sx={{
                  p: 2,
                  bgcolor: 'grey.50',
                  borderRadius: 1,
                  whiteSpace: 'pre-wrap',
                  fontFamily: 'monospace',
                }}
              >
                {result}
              </Box>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default DocumentGenerator;
