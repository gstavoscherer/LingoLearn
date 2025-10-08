import type { PageLoad } from './$types';
import type { TextType } from '$lib/types';

function formatText(raw: any): TextType {
    return {
        id: raw.id,
        title: raw.title,
        author: raw.author,
        language: raw.language,
        totalWords: raw.total_words,
        totalKnowWords: raw.total_know_words,
        lastPage: raw.last_page,
        totalPages: raw.total_pages,
        imagePath: raw.image_path ?? undefined
    };
}

export const load = (async ({ fetch, params, parent }) => {
    const { token } = await parent();
    const { text_id, page_number } = params;

    const res = await fetch(`${import.meta.env.VITE_API_URL}/texts/${text_id}/pages/${page_number}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    const page = await res.json();

    const formattedPage = {
        ...page,
        text: formatText(page.text) // só formata o text
    };

    return { data: formattedPage };
}) satisfies PageLoad;
