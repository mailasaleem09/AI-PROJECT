import React, { useEffect, useState } from 'react';
import { Container, Typography, Grid, Paper, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);

    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (!storedUser) {
            navigate('/login');
        } else {
            setUser(JSON.parse(storedUser));
        }
    }, [navigate]);

    if (!user) return null;

    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Typography variant="h4" gutterBottom>
                Welcome, {user.name}
            </Typography>
            <Grid container spacing={3}>
                <Grid item xs={12} md={6} lg={4}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 200, justifyContent: 'center', alignItems: 'center' }}>
                        <Typography variant="h6" gutterBottom>New Prediction</Typography>
                        <Button variant="contained" onClick={() => navigate('/predict')}>
                            Start Checkup
                        </Button>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={6} lg={4}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 200, justifyContent: 'center', alignItems: 'center' }}>
                        <Typography variant="h6" gutterBottom>Your History</Typography>
                        <Button variant="outlined" onClick={() => navigate('/history')}>
                            View Reports
                        </Button>
                    </Paper>
                </Grid>
                {/* Placeholder for future features */}

            </Grid>
        </Container>
    );
};

export default Dashboard;
