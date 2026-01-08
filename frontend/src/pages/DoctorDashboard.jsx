import React, { useEffect, useState } from 'react';
import { Container, Typography, Paper, List, ListItem, ListItemText, Divider, Alert, CircularProgress, Grid, Box } from '@mui/material';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import api from '../api/axios';

const DoctorDashboard = () => {
    const [patients, setPatients] = useState([]);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [patientsRes, statsRes] = await Promise.all([
                    api.get('/doctor/predictions'),
                    api.get('/stats')
                ]);
                setPatients(patientsRes.data);
                setStats(statsRes.data);
            } catch (err) {
                console.error("Failed to fetch doctor data", err);
                setError("Failed to load dashboard data.");
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return <Container sx={{ mt: 4, textAlign: 'center' }}><CircularProgress /></Container>;
    if (error) return <Container sx={{ mt: 4 }}><Alert severity="error">{error}</Alert></Container>;

    const accuracyData = stats ? [
        { name: 'Correct', value: parseFloat((stats.accuracy * 100).toFixed(1)) },
        { name: 'Incorrect', value: parseFloat((100 - (stats.accuracy * 100)).toFixed(1)) }
    ] : [];

    const COLORS = ['#0088FE', '#FF8042'];

    return (
        <Container maxWidth="lg" sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>Doctor Dashboard</Typography>

            <Grid container spacing={3}>
                <Grid item xs={12} md={5}>
                    <Paper elevation={3} sx={{ p: 2, height: 400, display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative' }}>
                        <Typography variant="h6" gutterBottom>Model Accuracy</Typography>
                        {stats ? (
                            <>
                                <Box sx={{ width: '100%', height: '80%' }}>
                                    <ResponsiveContainer>
                                        <PieChart>
                                            <Pie
                                                data={accuracyData}
                                                cx="50%"
                                                cy="50%"
                                                innerRadius={60}
                                                outerRadius={90}
                                                fill="#8884d8"
                                                paddingAngle={5}
                                                dataKey="value"
                                                label
                                            >
                                                {accuracyData.map((entry, index) => (
                                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                                ))}
                                            </Pie>
                                            <Tooltip />
                                            <Legend verticalAlign="bottom" height={36} />
                                        </PieChart>
                                    </ResponsiveContainer>
                                </Box>
                                <Box
                                    sx={{
                                        position: 'absolute',
                                        top: '50%',
                                        left: '50%',
                                        transform: 'translate(-50%, -20%)',
                                        textAlign: 'center',
                                        pointerEvents: 'none'
                                    }}
                                >
                                    <Typography variant="h3" fontWeight="bold" color="primary">
                                        {accuracyData[0].value}%
                                    </Typography>
                                    <Typography variant="caption" color="textSecondary">Accuracy</Typography>
                                </Box>
                                <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>{stats.model_type}</Typography>
                            </>
                        ) : (
                            <Typography variant="body1">No stats available</Typography>
                        )}
                    </Paper>
                </Grid>

                <Grid item xs={12} md={7}>
                    <Paper elevation={3} sx={{ p: 2, height: 400, overflow: 'auto' }}>
                        <Typography variant="h6" gutterBottom>Recent Patient Activity</Typography>

                        {patients.length === 0 ? (
                            <Typography variant="body1" sx={{ p: 2, fontStyle: 'italic', color: 'text.secondary' }}>
                                No patient records found.
                            </Typography>
                        ) : (
                            <List>
                                {patients.map((record, index) => (
                                    <React.Fragment key={record._id?.$oid || index}>
                                        <ListItem alignItems="flex-start">
                                            <ListItemText
                                                primary={
                                                    <Typography variant="subtitle1" fontWeight="bold">
                                                        {record.patient_name} — Diagnosis: {record.prediction}
                                                    </Typography>
                                                }
                                                secondary={
                                                    <>
                                                        <Typography component="span" variant="body2" color="text.primary">
                                                            Date: {new Date(record.timestamp?.$date || Date.now()).toLocaleDateString()}
                                                        </Typography>
                                                        {" — " + (record.recommendation || "Review required")}
                                                    </>
                                                }
                                            />
                                        </ListItem>
                                        {index < patients.length - 1 && <Divider component="li" />}
                                    </React.Fragment>
                                ))}
                            </List>
                        )}
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
};

export default DoctorDashboard;
