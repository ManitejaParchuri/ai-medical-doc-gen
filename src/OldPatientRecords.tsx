import React, { useState, useEffect } from "react";
import { Container, TextField, Button, Typography, Box, Select, MenuItem } from "@mui/material";
import axios from "axios";
import { useNavigate } from "react-router-dom";  // Import for navigation

const OldPatientRecords: React.FC = () => {
  const [patientId, setPatientId] = useState("");
  const [availablePatients, setAvailablePatients] = useState<string[]>([]);
  const [medicalRecord, setMedicalRecord] = useState("");
  const navigate = useNavigate();  // Hook to handle navigation

  // Fetch available patient IDs on load
  useEffect(() => {
    axios.get("http://localhost:8000/get-patient-ids").then((response) => {
      setAvailablePatients(response.data.patient_ids);
    });
  }, []);

  const handleFetchRecords = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/get-patient-records/${patientId}`);
      setMedicalRecord(response.data.medical_record);
    } catch (error) {
      console.error("Error fetching records:", error);
      setMedicalRecord("Error fetching medical records.");
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h5" gutterBottom>
        Retrieve Old Patient Records
      </Typography>

      <Select fullWidth value={patientId} onChange={(e) => setPatientId(e.target.value)}>
        {availablePatients.map((id) => (
          <MenuItem key={id} value={id}>
            {id}
          </MenuItem>
        ))}
      </Select>

      <Box mt={2} display="flex" gap={2}>
        <Button variant="contained" color="primary" onClick={handleFetchRecords}>
          Fetch Records
        </Button>

        {/* New Button to Navigate to New Patient Form */}
        <Button variant="contained" color="secondary" onClick={() => navigate("/new-patient")}>
          New Patient
        </Button>
      </Box>

      <Box mt={3} sx={{ p: 2, border: "1px solid #ccc", borderRadius: 2, backgroundColor: "#f9f9f9", maxHeight: "400px", overflowY: "auto" }}>
        <pre style={{ whiteSpace: "pre-wrap", wordWrap: "break-word" }}>
          {medicalRecord || "Patient records will show here..."}
        </pre>
      </Box>
    </Container>
  );
};

export default OldPatientRecords;
