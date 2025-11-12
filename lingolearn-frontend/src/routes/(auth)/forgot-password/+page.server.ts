import { fail, redirect, type Actions } from '@sveltejs/kit';
import { API_URL } from '$lib/config/api';

export const actions: Actions = {
    recover: async ({ request, cookies }) => {
        const data = await request.formData();

        const body = {
            email: data.get('email')?.toString(),
        }

        const res = await fetch(`${API_URL}/auth/request-password-reset`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        })

        if (!res.ok) {
            fail(res.status, {erro: res.statusText});
        }

        cookies.set('flash', JSON.stringify({
            type: 'success',
            message: 'O email para redefinir sua senha foi enviado!'
        }), {
            path: '/',
            maxAge: 5
        });

        throw redirect(303, '/login');
    }
}