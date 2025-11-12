<script lang="ts">
	import StatCard from '$lib/components/ui/StatCard.svelte';
	import { BookMarked, BookOpen, StarIcon, TrendingUp } from '@lucide/svelte';
	import type { PaginatedList, SelectOptions, UserWordType } from '$lib/types';
	import { Card, SidebarWordDetail } from '$lib/components/layout';
	import type { PageProps } from './$types';
	import { Input } from '$lib/components/ui';
	import Search from '$lib/components/ui/Search.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { goto, invalidateAll } from '$app/navigation';
	import UserWordList from '$lib/components/userWord/UserWordList.svelte';
	import { page } from '$app/state';
	import { getToastState } from '$lib/toast-state.svelte';
	import Pagination from '$lib/components/ui/Pagination.svelte';

	const toastState = getToastState();

	interface Filter {
		search: string;
		languageId: string;
		wordStatus: string;
		currentPage: number;
	}

	let filter: Filter = $state({ search: '', languageId: '0', wordStatus: '0', currentPage: 1 });
	let isDetailOpen = $state(false);

	let { data }: PageProps = $props();
	
	let stats = $derived(data.stats);

	let currentUserWord: UserWordType | undefined = $state();

	let userWords: PaginatedList<UserWordType> = $derived({
		currentPage: data.pagination.currentPage,
		perPage: data.pagination.perPage,
		totalPages: data.pagination.totalPages,
		items: data.userWords
	});

	let wordStatusOptions: SelectOptions[] = [
		{ label: 'Nova', value: 'new' },
		{ label: 'Aprendendo', value: 'learning' },
		{ label: 'Dominada', value: 'known' }
	];

	function searchOnClick() {
		const params = new URLSearchParams();

		if (filter.search) {
			params.set('query', filter.search);
		}

		if (filter.wordStatus !== '0') {
			params.set('status', filter.wordStatus);
		}

		if (filter.languageId !== '0') {
			params.set('languageId', filter.languageId);
		}

		if (filter.currentPage !== 0) {
			params.set('page', filter.currentPage.toString());
		}

		const query = params.toString();
		goto(query ? `?${query}` : '?', {
			replaceState: true,
			keepFocus: true
		});
	}

	function clearFilters() {
		filter.languageId = '0';
		filter.wordStatus = '0';
		filter.search = '';
		searchOnClick();
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

	function handleOnClick(userWord: UserWordType) {
		currentUserWord = userWord;
		isDetailOpen = true;
	}

	async function handleDeleteOnClick(wordId: number) {
		await fetch(`${import.meta.env.VITE_API_URL}/user-words/${page.data.user.id}/${wordId}`, {
			method: 'DELETE'
		});

		toastState.add('Sucesso', 'Palavra deletada!', 'success');
		await invalidateAll();
	}

	function handlePagination(page: number) {
		filter.currentPage = page;
		searchOnClick();
	}
</script>

{#if isDetailOpen && currentUserWord}
	<SidebarWordDetail
		userWord={currentUserWord}
		isOpen={isDetailOpen}
		onToggle={() => (isDetailOpen = !isDetailOpen)}
		saveOnClick={handleSaveOnClick}
		isEdit={true}
	/>
{/if}

{#snippet header()}
	<div class="header">
		<h2>Palavras salvas</h2>
		<div class="stats">
			<StatCard
				statCard={{ icon: BookOpen, primary: stats.total, secondary: 'Total' }}
			/>
			<StatCard
				statCard={{
					icon: TrendingUp,
					primary: stats.known,
					secondary: 'Dominadas'
				}}
			/>
			<StatCard
				statCard={{
					icon: StarIcon,
					primary: stats.learning,
					secondary: 'Aprendendo'
				}}
			/>
			<StatCard
				statCard={{ icon: BookMarked, primary: stats.new, secondary: 'Nova' }}
			/>
		</div>
	</div>
{/snippet}
{#snippet options()}
	<div class="options">
		<Search
			placeholder="Buscar por palavras ou traduções"
			size="full-width"
			bind:value={filter.search}
		/>
		<Input
			placeholder="Todos os idiomas"
			fieldType="select"
			options={data.languageOptions}
			bind:value={filter.languageId}
		/>
		<Input
			placeholder="Todos os status"
			fieldType="select"
			options={wordStatusOptions}
			bind:value={filter.wordStatus}
		/>
		<Button onclick={searchOnClick} style="padding: 0rem 2rem;">Buscar</Button>
		<Button onclick={clearFilters} variant="secondary" style="padding: 0rem 2rem;">
			Limpar filtros
		</Button>
	</div>
{/snippet}
<main>
	<section>
		<Card {header} {options} />
	</section>
	<section class="words-grid">
		<UserWordList userWords={data.userWords} {handleOnClick} {handleDeleteOnClick} />
	</section>
	<section>
		{#if data.userWords}
			<div class="pagination">
				<Pagination list={userWords} onPageChange={handlePagination} />
			</div>
		{/if}
	</section>
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
	}

	section {
		width: 100%;
		margin-bottom: 1rem;
	}

	.header {
		width: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: 2rem;
	}

	.stats {
		width: 100%;
		display: flex;
		justify-content: space-around;
	}

	.options {
		display: flex;
		gap: 2rem;
		width: 100%;
	}

	.words-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 1.5rem;
	}
</style>
