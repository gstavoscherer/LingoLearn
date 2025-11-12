import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import { API_URL } from '$lib/config/api';

export const load = (async ({ cookies }) => {
	const token = cookies.get('token');

	if (!token) {
		throw redirect(303, '/login');
	}

	try {
		const res = await fetch(`${API_URL}/auth/`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${token}`
			}
		});

		if (!res.ok) {
			throw redirect(303, '/login');
		}

		const userData = await res.json();
		const transformedUser = {
			id: userData.sub,
			email: userData.email,
			username: userData.username,
			lastVisitedTextId: userData.last_visited_text_id,
			translationLanguageId: userData.translation_language_id
		};

		return {
			user: transformedUser,
			isAuthenticated: true,
			token: token
		};
	} catch {
		cookies.delete('token', { path: '/' });

		throw redirect(303, '/login');
	}
}) satisfies LayoutServerLoad;
