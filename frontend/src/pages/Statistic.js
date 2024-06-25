import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { Bar, Pie } from 'react-chartjs-2';
import { Box, Button, FormControl, InputLabel, MenuItem, Select, CircularProgress } from '@mui/material';

const Statistic = () => {
    const [statistics, setStatistics] = useState([]);
    const [pageId, setPageId] = useState('');
    const [selectedPage, setSelectedPage] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchStatistics = useCallback(() => {
        axios.get('/api/v2/statistics')
            .then(response => {
                setStatistics(response.data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    const fetchPageStatistics = useCallback((id) => {
        setLoading(true);
        axios.get(`/api/v2/statistics/${id}`)
            .then(response => {
                setSelectedPage(response.data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    useEffect(() => {
        fetchStatistics();
    }, [fetchStatistics]);

    const handlePageSelect = (event) => {
        setPageId(event.target.value);
    };

    const handleSubmit = () => {
        if (pageId) {
            fetchPageStatistics(pageId);
        }
    };

    const pieChartData = {
        labels: statistics.map(page => page.title),
        datasets: [{
            data: statistics.map(page => page.total_length),
            backgroundColor: statistics.map((_, index) => `hsl(${index * 40}, 70%, 50%)`),
        }],
    };

    const barChartData = (field) => ({
        labels: statistics.map(page => page.title),
        datasets: [{
            label: field.replace('_', ' ').toUpperCase(),
            data: statistics.map(page => page[field]),
            backgroundColor: statistics.map((_, index) => `hsl(${index * 40}, 70%, 50%)`),
        }],
    });

    const barChartOptions = {
        scales: {
            x: {
                ticks: {
                    display: false
                },
                grid: {
                    display: false
                }
            },
            y: {
                ticks: {
                    display: false
                },
                grid: {
                    display: false
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        },
        maintainAspectRatio: false
    };

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <CircularProgress />
            </Box>
        );
    }

    return (
        <div className="statistics-page" style={{ width: '900px', margin: '0 auto' }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3, marginTop: 4 }}>
                <FormControl fullWidth sx={{ maxWidth: 600 }}>
                    <InputLabel id="page-select-label">Select Page</InputLabel>
                    <Select
                        labelId="page-select-label"
                        value={pageId}
                        onChange={handlePageSelect}
                    >
                        {statistics.map(page => (
                            <MenuItem key={page.id} value={page.id}>
                                {page.title}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <Button variant="contained" color="primary" onClick={handleSubmit}>
                    Submit
                </Button>
            </Box>

            {selectedPage && (
                <Box sx={{ marginTop: 4 }}>
                    <h2>Statistics for {selectedPage.title}</h2>
                    <p>{selectedPage.description}</p>
                    <p>Tags Count: {selectedPage.tags_count}</p>
                    <p>Description Length: {selectedPage.description_length}</p>
                    <p>Title Length: {selectedPage.title_length}</p>
                    <p>Total Length: {selectedPage.total_length}</p>
                    <p>Privacy Status: {selectedPage.privacy_status}</p>
                </Box>
            )}

            {statistics.length > 0 && (
                <>
                    <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 4 }}>
                        <div style={{ width: '50%' }}>
                            <h3>Pages Total Length Distribution</h3>
                            <Pie data={pieChartData} />
                        </div>
                    </Box>

                    <Box sx={{ display: 'flex', justifyContent: 'space-around', marginTop: 4 }}>
                        <div style={{ width: '30%' }}>
                            <h3>Tags Count</h3>
                            <Bar data={barChartData('tags_count')} options={barChartOptions} />
                        </div>
                        <div style={{ width: '30%' }}>
                            <h3>Title Length</h3>
                            <Bar data={barChartData('title_length')} options={barChartOptions} />
                        </div>
                        <div style={{ width: '30%' }}>
                            <h3>Description Length</h3>
                            <Bar data={barChartData('description_length')} options={barChartOptions} />
                        </div>
                    </Box>
                </>
            )}
        </div>
    );
};

export default Statistic;
