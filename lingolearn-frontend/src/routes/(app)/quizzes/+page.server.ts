import type { PageServerLoad } from './$types';
import { snakeToCamel } from '$lib/utils';
import type { QuizResponse } from '$lib/types';
import { fail } from '@sveltejs/kit';

export const load = (async ({ cookies, fetch }) => {
	const token = cookies.get('token');

	const request = await fetch(`${import.meta.env.VITE_API_URL}/quiz`, {
		method: 'GET',
		headers: {
			authorization: `Bearer ${token}`
		}
	});

	if (!request.ok) {
		throw new Error(`Failed to fetch quiz: ${request.status}`);
	}

	const { quiz } = await request.json();

	const camelCaseData = snakeToCamel<QuizResponse>(quiz).map((item) => ({
		...item,
		quality: 5
	}));

	return {
		quiz: camelCaseData
	};
}) satisfies PageServerLoad;

export const actions = {
	submitQuiz: async ({ request, cookies, fetch }) => {
		try {
			const token = cookies.get('token');
			
			const formData = await request.formData();
			const responses = formData.get('responses');
			
			if (!responses || typeof responses !== 'string') {
				return fail(400, { error: 'Dados de respostas inválidos' });
			}

			let responsesArray;
			try {
				responsesArray = JSON.parse(responses);
			} catch (parseError) {
				console.error('Erro ao fazer parse do JSON:', parseError);
				return fail(400, { error: 'Formato JSON inválido' });
			}

			if (!Array.isArray(responsesArray)) {
				return fail(400, { error: 'Respostas devem ser um array' });
			}

			const res = await fetch(`${import.meta.env.VITE_API_URL}/quiz`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify(responsesArray)
			});

			if (!res.ok) {
				const errorData = await res.json().catch(() => ({ error: 'Erro desconhecido' }));
				return fail(res.status, { error: errorData.error || 'Erro ao submeter quiz' });
			}

			const result = await res.json();

			return {
				type: 'success',
				data: result
			};
			
		} catch (error) {
			console.error('Erro:', error);
			return fail(500, { error: 'Erro interno ao submeter o quiz' });
		}
	}
};
