import { fail, redirect, type Actions } from '@sveltejs/kit';

export const actions: Actions = {
    register: async ({ request }) => {
        const data = await request.formData();

        const body = {
            username: data.get('username')?.toString(),
            email: data.get('email')?.toString(),
            password: data.get('password')?.toString() 
        }

        const res = await fetch(`${import.meta.env.VITE_API_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        })

        if (!res.ok) {
            fail(res.status, {erro: res.statusText});
        }

        throw redirect(303, '/login?registered=1');
    }
}