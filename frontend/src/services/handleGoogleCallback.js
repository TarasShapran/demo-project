import {redirect} from 'react-router-dom';
import loginPage from "../pages/LoginPage";

export const handleGoogleCallback = async ({request}) => {
    const url = new URL(request.url);
    const code = url.searchParams.get('code');
    console.log(code)
    console.log(JSON.stringify({code}))
    if (code) {
        try {
            const response = await fetch('http://localhost/api/auth/google/', {
                method: 'POST',
                body: JSON.stringify({code}),
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            const jwtData = await response.json();

            if (jwtData.access_token) {
                localStorage.setItem('access_token', jwtData.access_token);
                localStorage.setItem('refreshToken', jwtData.refresh_token);
            } else {
                console.log("ERROR CANT RECEIVE TOKEN **********")
            }

            return redirect('/cars');
        } catch (err) {
            console.error('Authorization failed:', err);
            throw new Response('Bad request', {status: 400});
        }
    }

    throw new Response('Not Found', {status: 404});
};
