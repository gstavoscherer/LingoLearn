import { fail, redirect, type Actions } from '@sveltejs/kit';
import { API_URL } from '$lib/config/api';

export const actions: Actions = {
    register: async ({ request, cookies }) => {
        const data = await request.formData();
        const translation_language_id = parseInt((data.get('idioma-nativo') ?? '0').toString());

        if (!translation_language_id || translation_language_id == 0) {
            return fail(404, {error: "Por favor selecione um idioma."})
        }

        const body = {
            username: data.get('usuario')?.toString(),
            email: data.get('email')?.toString(),
            password: data.get('password')?.toString(),
            translation_language_id: translation_language_id
        }


        const res = await fetch(`${API_URL}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        })
    
        if (!res.ok) {
            const errorBody = await res.json();
            const error = errorBody.detail.error.message;
            return fail(res.status, {error: error});
        }

        cookies.set('flash', JSON.stringify({
            type: 'success',
            message: 'Conta criada com sucesso! Faça login para continuar.'
        }), {
            path: '/',
            maxAge: 5
        });

        throw redirect(303, '/login');
    }
}