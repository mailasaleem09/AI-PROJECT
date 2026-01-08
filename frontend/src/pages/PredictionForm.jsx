import React, { useState, useEffect } from 'react';
import { Container, Typography, TextField, Button, Box, Paper, FormControlLabel, Checkbox, Grid, Alert, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const PredictionForm = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    // Initial state for 24 features
    const initialFormData = {
        glucose: '', cholesterol: '', hemoglobin: '', platelets: '', white_blood_cells: '',
        red_blood_cells: '', hematocrit: '', mean_corpuscular_volume: '', mean_corpuscular_hemoglobin: '',
        mean_corpuscular_hemoglobin_concentration: '', insulin: '', bmi: '', systolic_blood_pressure: '',
        diastolic_blood_pressure: '', triglycerides: '', hba1c: '', ldl_cholesterol: '', hdl_cholesterol: '',
        alt: '', ast: '', heart_rate: '', creatinine: '', troponin: '', c_reactive_protein: ''
    };

    const [formData, setFormData] = useState(initialFormData);
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    // Auto-scroll to result when it arrives
    React.useEffect(() => {
        if (prediction) {
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }
    }, [prediction]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Validate that all fields have values
        const emptyFields = Object.entries(formData).filter(([key, value]) => value === '' || value == null);
        if (emptyFields.length > 0) {
            setError('Please fill in all fields before submitting.');
            return;
        }
        setLoading(true);
        setError('');
        setPrediction(null);
        try {
            const user = JSON.parse(localStorage.getItem('user'));
            const response = await api.post('/predict', {
                user_id: user ? user._id?.$oid || user.id : 'anonymous',
                symptoms: formData
            });
            setPrediction(response.data);
        } catch (err) {
            console.error("Prediction Error:", err);
            const errMsg = err.response?.data?.error || err.message || 'Unknown error occurred';
            setError(`Prediction failed: ${errMsg}`);
        } finally {
            setLoading(false);
        }
    };

    const featureLabels = {
        glucose: "Glucose", cholesterol: "Cholesterol", hemoglobin: "Hemoglobin", platelets: "Platelets",
        white_blood_cells: "White Blood Cells", red_blood_cells: "Red Blood Cells", hematocrit: "Hematocrit",
        mean_corpuscular_volume: "Mean Corpuscular Volume", mean_corpuscular_hemoglobin: "Mean Corpuscular Hemoglobin",
        mean_corpuscular_hemoglobin_concentration: "MCHC", insulin: "Insulin", bmi: "BMI",
        systolic_blood_pressure: "Systolic BP", diastolic_blood_pressure: "Diastolic BP", triglycerides: "Triglycerides",
        hba1c: "HbA1c", ldl_cholesterol: "LDL Cholesterol", hdl_cholesterol: "HDL Cholesterol",
        alt: "ALT", ast: "AST", heart_rate: "Heart Rate", creatinine: "Creatinine",
        troponin: "Troponin", c_reactive_protein: "C-Reactive Protein"
    };

    return (
        <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
            <Paper elevation={3} sx={{ p: 4 }}>
                <Typography variant="h4" gutterBottom align="center" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                    Medical Assessment
                </Typography>
                <Typography variant="body1" align="center" sx={{ mb: 4, color: 'text.secondary' }}>
                    Enter the patient's blood sample details below for AI analysis.
                </Typography>

                {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

                <Box component="form" onSubmit={handleSubmit}>
                    <Grid container spacing={2}>
                        {Object.keys(initialFormData).map((key) => (
                            <Grid item xs={12} sm={6} md={4} key={key}>
                                <TextField
                                    fullWidth
                                    label={featureLabels[key] || key}
                                    name={key}
                                    type="number"
                                    value={formData[key]}
                                    onChange={handleChange}
                                    variant="outlined"
                                    size="small"
                                />
                            </Grid>
                        ))}
                    </Grid>

                    <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
                        <Button
                            type="submit"
                            variant="contained"
                            size="large"
                            disabled={loading}
                            sx={{ minWidth: 200, py: 1.5 }}
                        >
                            {loading ? <CircularProgress size={24} /> : 'Analyze Sample'}
                        </Button>
                    </Box>
                </Box>

                {prediction && (
                    <Box sx={{ mt: 4, p: 3, bgcolor: '#f5f9ff', borderRadius: 2, border: '1px solid #e0e0e0' }}>
                        <Typography variant="h5" color="primary" gutterBottom>
                            Analysis Result
                        </Typography>
                        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                            Predicted Condition: {prediction.prediction}
                        </Typography>
                        <Typography variant="body1" sx={{ mt: 1 }}>
                            {prediction.recommendation}
                        </Typography>
                    </Box>
                )}
            </Paper>
        </Container>
    );
};

export default PredictionForm;
