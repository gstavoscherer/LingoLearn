import type { DashboardData, PaginatedList, TextType } from '$lib/types';
import type { PageLoad } from './$types';

export const load = (async ({ parent, fetch }) => {
	const { user, token } = await parent();
	
	// Buscar textos
	const textsQuery = new URLSearchParams({
		user_id: user.id.toString(),
		top: '3',
		order_by: 'descending'
	});

	const textsRes = await fetch(`${import.meta.env.VITE_API_URL}/texts/?${textsQuery}`);
	const textsData = await textsRes.json();

	// Buscar dados do dashboard com token no header
	const dashboardRes = await fetch(`${import.meta.env.VITE_API_URL}/dashboard`, {
		headers: {
			'Authorization': `Bearer ${token}`
		}
	});
	
	if (!dashboardRes.ok) {
		throw new Error(`Failed to fetch dashboard data: ${dashboardRes.status}`);
	}
	
	const dashboardDataRaw = await dashboardRes.json();

	// Processar textos
	const texts: PaginatedList<TextType> = {
		currentPage: 0,
		perPage: 0,
		totalPages: 0,
		items: []
	};

	if (textsData.texts) {
		for (const text of textsData.texts) {
			texts.currentPage = textsData.page;
			texts.perPage = textsData.per_page;
			texts.totalPages = textsData.total_pages;

			const formattedText: TextType = {
				id: text.id,
				author: text.author,
				title: text.title,
				language: text.language,
				totalWords: text.total_words,
				totalKnownWords: text.total_known_words,
				imagePath: text.image_path
					? `${import.meta.env.VITE_API_URL}/${text.image_path.replace(/[\\/]+/g, '/').replace(/^\/+/, '')}`
					: '/default_book.png',
				lastVisitedPage: text.last_visited_page,
				totalPages: text.total_pages
			};
			texts.items.push(formattedText);
		}
	}

	// Converter dashboard data de snake_case para camelCase
	const dashboardData: DashboardData = {
		userKnownWords: dashboardDataRaw.user_known_words,
		userKnownWordsLastWeek: dashboardDataRaw.user_known_words_last_week,
		streak: dashboardDataRaw.streak,
		lastLogin: dashboardDataRaw.last_login,
		studyTimeToday: dashboardDataRaw.study_time_today
	};

	return { texts, dashboardData };
}) satisfies PageLoad;

