// src/routes/seusuario/word/+page.server.ts
import { fail } from '@sveltejs/kit';
import { API_URL } from '$lib/config/api';

export const actions = {
	saveUserWord: async ({ request, cookies, fetch }) => {
		try {
			const token = cookies.get('token');

			const formData = await request.formData();
			const wordId = formData.get('word_id');
			const translation = formData.get('translation');
			const translationLanguageId = formData.get('translation_language_id');
			const context = formData.get('context');
			const contextTranslation = formData.get('context_translation');
            const easinessFactor = formData.get('easiness_factor');

			const body = {
				word_id: Number(wordId),
				easiness_factor: easinessFactor,
				translation: translation,
				translation_language_id: Number(translationLanguageId),
				context: context,
				context_translation: contextTranslation
			};

			const response = await fetch(`${API_URL}/user-words/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify(body)
			});

			if (!response.ok) {
				throw new Error('Erro ao salvar palavra');
			}

			return { success: true, message: 'Palavra salva com sucesso!' };
		} catch (error) {
			console.error('Erro:', error);
			return fail(500, { error: 'Erro ao salvar palavra' });
		}
	}
};
