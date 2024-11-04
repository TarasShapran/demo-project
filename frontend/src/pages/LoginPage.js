import {useForm} from "react-hook-form";
import {authService} from "../services/authService";
import {useNavigate} from "react-router-dom";

const LoginPage = () => {
    const {register, handleSubmit} = useForm();
    const navigate = useNavigate();

    const login = async (user) => {
        await authService.login(user)
        navigate('/cars')
    }

    return (
        <form onSubmit={handleSubmit(login)}>
            <input type="text" placeholder={'email'} {...register('email')}/>
            <input type="text" placeholder={'password'} {...register('password')}/>
            <button>login</button>
        </form>
    );
};

export {LoginPage};