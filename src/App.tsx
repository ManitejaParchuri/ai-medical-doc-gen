import React, { useState } from 'react';
import { Container, Grid, TextField, Button, Typography, Box } from '@mui/material';
import axios from 'axios';

const App: React.FC = () => {
  const [nurseNotes, setNurseNotes] = useState('');
  const [dentistNotes, setDentistNotes] = useState('');
  const [aiOutput, setAiOutput] = useState('');

  const handleProcessNotes = async () => {
    try {
      const response = await axios.post('http://localhost:8000/process-notes', {
        nurse_notes: nurseNotes,
        dentist_notes: dentistNotes,
      });
      setAiOutput(response.data.ai_output);
    } catch (error) {
      console.error('Error processing notes:', error);
      setAiOutput('Error processing notes');
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Grid container spacing={4}>
        
        {/* Input Section */}
        <Grid item xs={12} md={6}>
          <Box mb={3}>
            <Typography variant="h6" color="primary" gutterBottom>
              Nurse's notes
            </Typography>
            <TextField
              fullWidth
              multiline
              minRows={6}
              placeholder="Enter nurse's observations and notes here..."
              variant="outlined"
              value={nurseNotes}
              onChange={(e) => setNurseNotes(e.target.value)}
            />
          </Box>
          
          <Box mb={3}>
            <Typography variant="h6" color="primary" gutterBottom>
              Dentist's observations and notes
            </Typography>
            <TextField
              fullWidth
              multiline
              minRows={6}
              placeholder="Connect your lapel mic and record the entire appointment..."
              variant="outlined"
              value={dentistNotes}
              onChange={(e) => setDentistNotes(e.target.value)}
            />
          </Box>

          <Box display="flex" gap={2}>
            <Button variant="contained" color="primary" onClick={handleProcessNotes}>
              PROCESS NOTES
            </Button>
          </Box>
        </Grid>

        {/* Output Section */}
        <Grid item xs={12} md={6}>
          <Typography variant="h6" color="primary" gutterBottom>
            AI Output
          </Typography>
          <TextField
            fullWidth
            multiline
            minRows={12}
            placeholder="Notes will show here..."
            variant="outlined"
            value={aiOutput}
            InputProps={{ readOnly: true }}
          />
        </Grid>

      </Grid>
    </Container>
  );
};

export default App;
