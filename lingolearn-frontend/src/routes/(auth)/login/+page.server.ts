import { fail, redirect, error, type Actions } from '@sveltejs/kit';

export const actions: Actions = {
  login: async ({ request, cookies }) => {
    const form = await request.formData();
    const email = form.get('email')?.toString().trim();
    const password = form.get('password')?.toString().trim();

    if (!email || !password) {
      return fail(400, { error: 'Todos os campos são obrigatórios.', success: false });
    }

    try {
      const body = new URLSearchParams({ username: email, password });

      const res = await fetch(`${import.meta.env.VITE_API_URL}/auth`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body.toString()
      });

      const result = await res.json();

      if (!res.ok) {
        const errorMessage =
          result?.detail?.error?.message ||
          result?.detail?.message ||
          'Erro desconhecido';

        if (res.status >= 400 && res.status < 500) {
          return fail(res.status, { error: 'Login inválido', success: false });
        }
        throw error(res.status, errorMessage);
      }

      cookies.set('token', result.access_token, {
        path: '/',
        httpOnly: true,
        sameSite: 'lax',
        secure: import.meta.env.PROD === true,
        maxAge: Number(import.meta.env.VITE_ACCESS_TOKEN_EXPIRE)
      });

    } catch (err) {
      console.error('Erro ao autenticar:', err);
      throw error(500, 'Erro ao processar a solicitação.');
    }
    
    throw redirect(303, '/home');
  }
};