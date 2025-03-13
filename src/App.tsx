// import React, { useState } from 'react';
// import { Container, Grid, TextField, Button, Typography, Box } from '@mui/material';
// import axios from 'axios';

// const App: React.FC = () => {
//   const [patientId, setPatientId] = useState('');
//   const [nurseNotes, setNurseNotes] = useState('');
//   const [dentistNotes, setDentistNotes] = useState('');
//   const [aiOutput, setAiOutput] = useState('');

//   const handleProcessNotes = async () => {
//     try {
//       const response = await axios.post('http://localhost:8000/process-notes', {
//         patient_id: patientId,  // Include the patient ID
//         nurse_notes: nurseNotes,
//         dentist_notes: dentistNotes,
//       });

//       setAiOutput(response.data.ai_output);
//     } catch (error) {
//       console.error('Error processing notes:', error);
//       setAiOutput('Error processing notes');
//     }
//   };

//   return (
//     <Container maxWidth="lg" sx={{ py: 4 }}>
//       <Grid container spacing={4}>
        
//         {/* Input Section */}
//         <Grid item xs={12} md={6}>
//           <Box mb={3}>
//             <Typography variant="h6" color="primary" gutterBottom>
//               Patient ID
//             </Typography>
//             <TextField
//               fullWidth
//               placeholder="Enter patient ID"
//               variant="outlined"
//               value={patientId}
//               onChange={(e) => setPatientId(e.target.value)}
//             />
//           </Box>

//           <Box mb={3}>
//             <Typography variant="h6" color="primary" gutterBottom>
//               Nurse's Notes
//             </Typography>
//             <TextField
//               fullWidth
//               multiline
//               minRows={6}
//               placeholder="Enter nurse's observations and notes here..."
//               variant="outlined"
//               value={nurseNotes}
//               onChange={(e) => setNurseNotes(e.target.value)}
//             />
//           </Box>
          
//           <Box mb={3}>
//             <Typography variant="h6" color="primary" gutterBottom>
//               Dentist's Observations and Notes
//             </Typography>
//             <TextField
//               fullWidth
//               multiline
//               minRows={6}
//               placeholder="Enter dentist's observations and notes here..."
//               variant="outlined"
//               value={dentistNotes}
//               onChange={(e) => setDentistNotes(e.target.value)}
//             />
//           </Box>

//           <Box display="flex" gap={2}>
//             <Button variant="contained" color="primary" onClick={handleProcessNotes}>
//               Process Notes
//             </Button>
//           </Box>
//         </Grid>

//         {/* Output Section */}
//         <Grid item xs={12} md={6}>
//           <Typography variant="h6" color="primary" gutterBottom>
//             Generated Medical Document
//           </Typography>
//           <Box 
//             sx={{ 
//               p: 2, 
//               border: '1px solid #ccc', 
//               borderRadius: 2, 
//               backgroundColor: '#f9f9f9',
//               maxHeight: '400px',
//               overflowY: 'auto'
//             }}
//           >
//             <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
//               {aiOutput || "Notes will show here..."}
//             </pre>
//           </Box>
//         </Grid>

//       </Grid>
//     </Container>
//   );
// };

// export default App;


import React from "react";
import { Container, Grid, Button, Typography, Box } from "@mui/material";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import NewPatientForm from "./NewPatientForm";
import OldPatientRecords from "./OldPatientRecords";

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="md" sx={{ py: 4, textAlign: "center" }}>
      <Typography variant="h4" gutterBottom>
        AI Medical Document Generation
      </Typography>
      <Box display="flex" justifyContent="center" gap={2} mt={4}>
        <Button variant="contained" color="primary" onClick={() => navigate("/old-patient-records")}>
          Old Patient Records
        </Button>
        <Button variant="contained" color="secondary" onClick={() => navigate("/new-patient")}>
          New Patient
        </Button>
      </Box>
    </Container>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/new-patient" element={<NewPatientForm />} />
        <Route path="/old-patient-records" element={<OldPatientRecords />} />
      </Routes>
    </Router>
  );
};

export default App;

