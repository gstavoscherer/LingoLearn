import type { PageLoad } from './$types';
import type { TextPageType, UserWordResponse, UserWordType } from '$lib/types';

export const load = (async ({ fetch, params, parent }) => {
	const { token } = await parent();
	const { text_id, page_number } = params;

	// Requisição para salvar última página lida do texto e último texto acessado do usuário
	await fetch(
		`${import.meta.env.VITE_API_URL}/texts/${text_id}/track-page?page_number=${page_number}`,
		{
			method: 'POST',
			headers: {
				Authorization: `Bearer ${token}`
			}
		}
	);

	// Requisição do TextPage
	const textPageResponse = await fetch(
		`${import.meta.env.VITE_API_URL}/texts/${text_id}/pages/${page_number}`,
		{
			headers: {
				Authorization: `Bearer ${token}`
			}
		}
	);

	const textPageResponseJson = await textPageResponse.json();

	const textPage: TextPageType = {
		text: {
			id: textPageResponseJson.text.id,
			author: textPageResponseJson.text.author,
			title: textPageResponseJson.text.title,
			language: textPageResponseJson.text.language,
			lastVisitedPage: textPageResponseJson.text.last_visited_page,
			totalKnownWords: textPageResponseJson.text.total_known_words,
			totalPages: textPageResponseJson.text.total_pages,
			totalWords: textPageResponseJson.text.total_words,
			imagePath: textPageResponseJson.text.image_path ?? '/default_book.png'
		},
		page: {
			id: textPageResponseJson.page.id,
			textId: textPageResponseJson.page.text_id,
			number: textPageResponseJson.page.number,
			content: textPageResponseJson.page.content
		}
	};

	// Requisição para UserWords
	const languageId = textPage.text.language.id;
	const UserWordResponse = await fetch(
		`${import.meta.env.VITE_API_URL}/user-words?language_id=${languageId}&per_page=99999999`,
		{
			headers: {
				Authorization: `Bearer ${token}`
			}
		}
	);

	const userWordsResponseJson = await UserWordResponse.json();

	

	const userWords: UserWordType[] = userWordsResponseJson.pagination.items.map((item: UserWordResponse) => ({
		userId: item.user_id,
		easinessFactor: item.easiness_factor,
		translation: item.translation,
		translationLanguageId: item.translation_language_id,
		context: item.context,
		contextTranslation: item.context_translation,
		lastReview: item.last_review ? new Date(item.last_review) : undefined,
		nextReview: item.next_review ? new Date(item.next_review) : undefined,
		isNew: false,
		word: {
			id: item.word.id,
			word: item.word.word,
			languageId: item.word.language_id,
			category: item.word.category
		}
	}));

	return { data: { textPage, userWords } };
}) satisfies PageLoad;
