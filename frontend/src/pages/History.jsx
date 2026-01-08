import React, { useEffect, useState } from 'react';
import { Container, Typography, Paper, List, ListItem, ListItemText, Divider, Chip } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const History = () => {
    const navigate = useNavigate();
    const [history, setHistory] = useState([]);
    const [user, setUser] = useState(null);

    useEffect(() => {
        const fetchHistory = async () => {
            const storedUser = localStorage.getItem('user');
            if (storedUser) {
                const parsedUser = JSON.parse(storedUser);
                setUser(parsedUser);
                try {
                    const userId = parsedUser._id?.$oid || parsedUser.id;
                    const response = await api.get(`/history/${userId}`);
                    setHistory(response.data);
                } catch (error) {
                    console.error("Failed to load history", error);
                }
            } else {
                navigate('/login');
            }
        };
        fetchHistory();
    }, [navigate]);

    return (
        <Container maxWidth="md" sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>Prediction History</Typography>
            <Paper elevation={3}>
                <List>
                    {history.length === 0 ? (
                        <ListItem><ListItemText primary="No history found." /></ListItem>
                    ) : (
                        history.map((item, index) => (
                            <React.Fragment key={index}>
                                <ListItem alignItems="flex-start">
                                    <ListItemText
                                        primary={
                                            <Typography component="span" variant="h6" color="primary">
                                                {item.prediction_result}
                                            </Typography>
                                        }
                                        secondary={
                                            <>
                                                <Typography component="span" variant="body2" color="text.primary">
                                                    Date: {new Date(item.created_at?.$date || item.created_at).toLocaleDateString()}
                                                </Typography>
                                                <br />
                                                Symptoms: Age {item.input_data.age},
                                                Fever: {item.input_data.fever ? 'Yes' : 'No'},
                                                Cough: {item.input_data.cough ? 'Yes' : 'No'}
                                            </>
                                        }
                                    />
                                </ListItem>
                                {index < history.length - 1 && <Divider component="li" />}
                            </React.Fragment>
                        ))
                    )}
                </List>
            </Paper>
        </Container>
    );
};

export default History;
