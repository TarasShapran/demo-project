// import {createBrowserRouter, Navigate} from "react-router-dom";
// import {MainLayout} from "./layouts/MainLayout";
// import {LoginPage} from "./pages/LoginPage";
// import {CarsPage} from "./pages/CarsPage";
//
// const router = createBrowserRouter([
//     {
//         path: '', element: <MainLayout/>, children: [
//             {index: true, element: <Navigate to={'login'}/>},
//             {path: 'login', element: <LoginPage/>},
//             {path: 'cars', element: <CarsPage/>}
//         ]
//     }
// ]);
//
// export {
//     router
// }

import React from 'react';
import {createBrowserRouter} from 'react-router-dom';
import {CarsPage} from './pages/CarsPage';
import LoginPage from './pages/LoginPage';
import {handleGoogleCallback} from './services/handleGoogleCallback';

const router = createBrowserRouter([
    {
        path: '/',
        element: <LoginPage/>,
    },
    {
        path: '/cars',
        element: <CarsPage/>,
    },
    {
        path: '/auth/callback',
        loader: handleGoogleCallback,
        element: <div>Loading...</div>, // Можна додати компонент для лоадера
    },
]);

export default router;