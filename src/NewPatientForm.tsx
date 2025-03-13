import React, { useState } from 'react';
import axios from 'axios';
import { Container, Grid, TextField, Button, Typography, Box } from '@mui/material';

const NewPatientForm: React.FC = () => {
  const [nurseNotes, setNurseNotes] = useState('');
  const [doctorNotes, setDoctorNotes] = useState('');
  const [summary, setSummary] = useState('');
  const [similarCases, setSimilarCases] = useState<any[]>([]); // Store similar cases

  const handleProcessNotes = async () => {
    try {
      const requestBody = {
        nurse_notes: nurseNotes.trim(),  // Ensure no empty spaces
        doctor_notes: doctorNotes.trim(), 
      };
  
      console.log("Sending request:", requestBody);  // Debugging log
  
      const response = await axios.post('http://localhost:8000/process-notes', requestBody, {
        headers: {
          "Content-Type": "application/json",
        },
      });
  
      setSummary(response.data.summary);
      setSimilarCases(response.data.similar_cases);
    } catch (error) {
      console.error("Error processing notes:", error);
      setSummary("Error processing notes");
      setSimilarCases([]);
    }
  };
  

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Grid container spacing={4}>
        
        {/* Input Section */}
        <Grid item xs={12} md={6}>
          <Box mb={3}>
            <Typography variant="h6" color="primary" gutterBottom>
              Nurse's Notes
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
              Doctor's Notes
            </Typography>
            <TextField
              fullWidth
              multiline
              minRows={6}
              placeholder="Enter doctor's observations and notes here..."
              variant="outlined"
              value={doctorNotes}
              onChange={(e) => setDoctorNotes(e.target.value)}
            />
          </Box>

          <Box display="flex" gap={2}>
            <Button variant="contained" color="primary" onClick={handleProcessNotes}>
              PROCESS NOTES
            </Button>
          </Box>
        </Grid>

        {/* AI-Generated Summary Section */}
        <Grid item xs={12} md={6}>
          <Typography variant="h6" color="primary" gutterBottom>
            AI-Generated Summary
          </Typography>
          <TextField
            fullWidth
            multiline
            minRows={6}
            placeholder="AI-generated summary will be displayed here..."
            variant="outlined"
            value={summary}
            InputProps={{ readOnly: true }}
          />
        </Grid>

        {/* Similar Cases Section */}
        {similarCases.length > 0 && (
          <Grid item xs={12}>
            <Typography variant="h6" color="primary" gutterBottom>
              Similar Cases Found
            </Typography>
            {similarCases.map((caseItem, index) => (
              <Box key={index} mb={2} p={2} border="1px solid #ddd" borderRadius="8px">
                <Typography><strong>Patient ID:</strong> {caseItem.patient_id}</Typography>
                <Typography><strong>Symptoms:</strong> {caseItem.symptoms}</Typography>
                <Typography><strong>Diagnosis:</strong> {caseItem.diagnosis}</Typography>
              </Box>
            ))}
          </Grid>
        )}
        
      </Grid>
    </Container>
  );
};

export default NewPatientForm;
