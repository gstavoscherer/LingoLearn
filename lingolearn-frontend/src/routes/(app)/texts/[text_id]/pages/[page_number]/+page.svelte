<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { page } from '$app/state';
	import { SidebarWordDetail } from '$lib/components/layout';
	import { Page, PageHeader } from '$lib/components/page';
	import Pagination from '$lib/components/ui/Pagination.svelte';
	import { getToastState } from '$lib/toast-state.svelte';
	import type { PaginatedList, TextPageType, UserWordType, WordStatus } from '$lib/types';
	import { sendStudyTime } from '$lib/utils';
	import { onMount } from 'svelte';

	const toastState = getToastState();

	let startTime = $state(0);

	let textPage: TextPageType = $derived(page.data.data.textPage);
	let userWords: UserWordType[] = $derived.by(() =>
		page.data?.data?.userWords?.map((word: UserWordType) => {
			const ef = word.easinessFactor;
			let status: WordStatus;

			if (ef <= 1.5) status = 'unknown';
			else if (ef <= 1.625) status = 'recognize';
			else if (ef <= 1.75) status = 'familiar';
			else if (ef <= 1.875) status = 'well-known';
			else status = 'known';

			return {
				...word,
				word: {
					...word.word,
					category: 'word',
					status
				}
			};
		})
	);

	let paginatedTextPage: PaginatedList<TextPageType> = $derived.by(() => {
		return {
			items: [textPage],
			currentPage: textPage.page.number,
			perPage: 1,
			totalPages: textPage.text.totalPages
		};
	});

	let isDetailOpen = $state(false);
	let currentUserWord: UserWordType | undefined = $state();

	onMount(() => {
		startTime = Date.now();

		return () => {
			const endTime = Date.now();
			const secondsSpent = Math.floor((endTime - startTime) / 1000);
			
			if (secondsSpent > 10) {
				sendStudyTime(secondsSpent, page.data.token);
			}
		};
	});

	function onWordClick(userWord: UserWordType) {
		currentUserWord = userWord;
		isDetailOpen = true;
	}

	function handlePageChange(page: number) {
		goto(`/texts/${textPage.text.id}/pages/${page}`);
	}

	async function handleSaveOnClick(starRating: number, isNew: boolean) {
		if (!currentUserWord) return;

		// Mapeamento mais limpo para easinessFactor
		const easinessFactors = { 1: 1.5, 2: 1.6, 3: 1.7, 4: 1.8, 5: 2.0 };
		const easinessFactor = easinessFactors[starRating as keyof typeof easinessFactors] || 1.5;

		// Cria um form e submete via action
		const formData = new FormData();
		formData.append('user_id', page.data.user.id);
		formData.append('word_id', currentUserWord.word.id?.toString() || '');
		formData.append('easiness_factor', easinessFactor.toString());
		formData.append('translation', currentUserWord.translation || '');
		formData.append(
			'translation_language_id',
			currentUserWord.translationLanguageId.toString()
		);
		formData.append('context', currentUserWord.context || '');
		formData.append('context_translation', currentUserWord.contextTranslation || '');

		// Determina a ação baseado se é novo ou edição
		const action = isNew ? 'saveUserWord' : 'saveUserWord';

		try {
			const response = await fetch(`?/${action}`, {
				method: 'POST',
				body: formData
			});

			const result = await response.json();

			if (result.type === 'success') {
				toastState.add('Sucesso!', 'Palavra salva!', 'success');
				await invalidateAll();
				isDetailOpen = false;
			} else {
				toastState.add('Erro', 'Ocorreu um erro ao salvar', 'error');
			}
		} catch (error) {
			console.error('Erro na requisição:', error);
			toastState.add('Erro', 'Ocorreu um erro ao salvar', 'error');
		}
	}
</script>

{#if isDetailOpen && currentUserWord}
	<SidebarWordDetail
		bind:isOpen={isDetailOpen}
		onToggle={() => (isDetailOpen = !isDetailOpen)}
		bind:userWord={currentUserWord}
		isEdit={true}
		saveOnClick={handleSaveOnClick}
	/>
{/if}

<div class="page">
	<PageHeader text={textPage.text} />

	<div class="page-content">
		<Page {textPage} {userWords} {onWordClick} />
	</div>
	<Pagination list={paginatedTextPage} onPageChange={handlePageChange} />
</div>

<style>
	.page {
		width: 100%;
		display: flex;
		flex-direction: column;
	}

	.page-content {
		display: flex;
		justify-content: center;
		padding: 1.5rem 0.5rem;
	}
</style>
