import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute = () => {
    // Check if user exists in local storage
    const user = JSON.parse(localStorage.getItem('user'));

    // If no user, redirect to login
    if (!user) {
        return <Navigate to="/login" replace />;
    }

    // If user exists, render the child routes (Outlet)
    return <Outlet />;
};

export default ProtectedRoute;
