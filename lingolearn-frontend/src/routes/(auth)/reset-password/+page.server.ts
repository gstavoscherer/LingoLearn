import { fail, redirect, type Actions } from '@sveltejs/kit';
import { API_URL } from '$lib/config/api';

export const actions: Actions = {
    reset: async ({ request, cookies }) => {
        const data = await request.formData();

        const body = {
            token: data.get('token')?.toString(),
            new_password: data.get('password')?.toString()
        }

        const res = await fetch(`${API_URL}/auth/confirm-password-reset`, {
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
            message: 'Sua senha foi alterada!'
        }), {
            path: '/',
            maxAge: 5
        });

        throw redirect(303, '/login');
    }
}