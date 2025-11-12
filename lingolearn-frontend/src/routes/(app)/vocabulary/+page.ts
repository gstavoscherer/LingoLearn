import type { LanguageType, UserWordResponse, UserWordType } from '$lib/types';
import type { PageLoad } from './$types';

export const load = (async ({ parent, fetch, url }) => {
	const { token } = await parent();

	// Pegar todos os parâmetros
	const statusFilter = url.searchParams.get('status') || undefined;
	const languageIdFilter = url.searchParams.get('languageId') || undefined;
	const page = url.searchParams.get('page') || '1';
	const query = url.searchParams.get('query') || undefined;

	const queryParams = new URLSearchParams({
		page: page,
		per_page: '8'
	});

	if (statusFilter) {
		queryParams.set('status', statusFilter);
	}

	if (languageIdFilter) {
		queryParams.set('language_id', languageIdFilter);
	}

	if (query) {
		queryParams.set('query', query);
	}

	const languagesRequest = await fetch(`${import.meta.env.VITE_API_URL}/languages/`);
	const languages: LanguageType[] = await languagesRequest.json();
	const languageOptions = languages.map((language) => {
		return { value: language.id.toString(), label: `${language.name} (${language.code})` };
	});

	// Fazer request com os filtros
	const userWordsRequest = await fetch(
		`${import.meta.env.VITE_API_URL}/user-words?${queryParams.toString()}`,
		{
			method: 'GET',
			headers: {
				Authorization: `Bearer ${token}`
			}
		}
	);

	if (!userWordsRequest.ok) {
		throw new Error('Failed to fetch user words');
	}

	const response = await userWordsRequest.json();

	// Mapear a resposta para o formato do frontend
	const userWords: UserWordType[] = response.pagination.items.map((item: UserWordResponse) => ({
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

	return {
		languageOptions,
		userWords,
		pagination: {
			currentPage: response.pagination.current_page,
			totalPages: response.pagination.total_pages,
			perPage: response.pagination.per_page,
			totalCount: response.pagination.total_count
		},
		stats: response.stats,
		filters: {
			status: statusFilter,
			languageId: languageIdFilter,
			page: parseInt(page)
		}
	};
}) satisfies PageLoad;
