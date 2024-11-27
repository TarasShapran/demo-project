// import {useForm} from "react-hook-form";
// import {authService} from "../services/authService";
// import {useNavigate} from "react-router-dom";
//
// const LoginPage = () => {
//     const {register, handleSubmit} = useForm();
//     const navigate = useNavigate();
//
//     const login = async (user) => {
//         await authService.login(user)
//         navigate('/cars')
//     }
//
//     return (
//         <form onSubmit={handleSubmit(login)}>
//             <input type="text" placeholder={'email'} {...register('email')}/>
//             <input type="text" placeholder={'password'} {...register('password')}/>
//             <button>login</button>
//         </form>
//     );
// };
//
// export {LoginPage};
//
//
// import React from 'react';
// import { googleCallbackUri, googleClientId } from '../constants/config';
//
// const LoginPage = () => {
//   const googleSignInUrl = `https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=${googleCallbackUri}&prompt=consent&response_type=code&client_id=${googleClientId}&scope=openid%20email%20profile&access_type=offline`;
//
//   return (
//     <div style={{ padding: 20 }}>
//       <a href={googleSignInUrl}>Sign in with Google</a>
//     </div>
//   );
// };
//
// export default LoginPage;


import React from 'react';
import {useForm} from 'react-hook-form';
import {authService} from '../services/authService';
import {useNavigate} from 'react-router-dom';
import {googleCallbackUri, googleClientId} from '../constants/config';

const LoginPage = () => {
    const {register, handleSubmit} = useForm();
    const navigate = useNavigate();

    const googleSignInUrl = `https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=${googleCallbackUri}&prompt=consent&response_type=code&client_id=${googleClientId}&scope=openid%20email%20profile&access_type=offline`;

    const login = async (user) => {
        try {
            await authService.login(user);
            navigate('/cars');
        } catch (error) {
            alert('Login failed. Please try again.');
    }
    };

    return (
        <div style={styles.container}>
            <h2 style={styles.title}>Welcome Back</h2>

            {/* Google Sign-In */}
            <div style={styles.googleContainer}>
                <a href={googleSignInUrl} style={styles.googleButton}>
                    <img
                        src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png"
                        alt="Google Logo"
                        style={styles.googleLogo}
                    />
                    Sign in with Google
                </a>
            </div>

            <div style={styles.divider}>or</div>

            {/* Regular Login Form */}
            <form onSubmit={handleSubmit(login)} style={styles.form}>
                <input
                    type="text"
                    placeholder="Email"
                    {...register('email', {required: true})}
                    style={styles.input}
                />
                <input
                    type="password"
                    placeholder="Password"
                    {...register('password', {required: true})}
                    style={styles.input}
                />
                <button type="submit" style={styles.submitButton}>
                    Login
                </button>
            </form>
        </div>
    );
};

const styles = {
    container: {
        maxWidth: '400px',
        margin: '50px auto',
        padding: '20px',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
        borderRadius: '8px',
        textAlign: 'center',
        backgroundColor: '#fff',
    },
    title: {
        fontSize: '24px',
        marginBottom: '20px',
        fontWeight: 'bold',
    },
    googleContainer: {
        marginBottom: '20px',
    },
    googleButton: {
        display: 'inline-flex',
        alignItems: 'center',
        padding: '10px 20px',
        borderRadius: '4px',
        backgroundColor: '#4285F4',
        color: '#fff',
        textDecoration: 'none',
        fontSize: '16px',
        fontWeight: 'bold',
    },
    googleLogo: {
        width: '20px',
        marginRight: '10px',
    },
    divider: {
        margin: '20px 0',
        fontSize: '14px',
        color: '#aaa',
        position: 'relative',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
    },
    input: {
        padding: '10px',
        fontSize: '16px',
        border: '1px solid #ccc',
        borderRadius: '4px',
    },
    submitButton: {
        padding: '10px',
        fontSize: '16px',
        backgroundColor: '#4CAF50',
        color: '#fff',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
    },
};

export default LoginPage;
