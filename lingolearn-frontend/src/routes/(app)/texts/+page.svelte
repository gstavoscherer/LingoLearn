<script lang="ts">
	import { page } from '$app/state';
	import { Button, TextList } from '$lib/components/ui';
	import { TextModal, TextModalEdit } from '$lib/components/modals';
	import { Search } from '$lib/components/ui';
	import type { TextType, PaginatedList, SelectOptions, LanguageType } from '$lib/types';
	import { Upload } from '@lucide/svelte';
	import { onMount } from 'svelte';
	import Pagination from '$lib/components/ui/Pagination.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import { searchStore } from '$lib/stores/search';
	import { Card } from '$lib/components/layout';

	interface Filter {
		languageId: string;
		orderBy?: string;
	}

	let filter: Filter = $state({ languageId: '0', orderBy: '0' });
	let search: string = $state('');

	let isShowTextModal: boolean = $state(false);
	let isShowTextModalEdit: boolean = $state(false);

	let languageOptions: SelectOptions[] | undefined = $state();
	let orderOptions: SelectOptions[] = [
		{ label: 'Recente', value: 'descending' },
		{ label: 'Mais Antigo', value: 'ascending' }
	];

	let texts: PaginatedList<TextType> = $state({
		currentPage: 0,
		perPage: 0,
		totalPages: 0,
		items: []
	});
	let currentText: TextType | undefined = $state();
	let currentPage: number = $state(0);

	function handleOnDetail(text: TextType) {
		currentText = text;
		isShowTextModalEdit = !isShowTextModalEdit;
	}

	function handleOnSave() {
		loadTexts();
	}

	function handlePagination(page: number) {
		currentPage = page;
		loadTexts();
	}

	function searchOnClick() {
		currentPage = 1;
		loadTexts();
	}

	function clearFilters() {
		filter.languageId = '0';
		filter.orderBy = '0';
		search = '';
		loadTexts();
	}
	async function loadTexts() {
		const BASE_URL = import.meta.env.VITE_API_URL;

		let userId = page.data.user.id;
		let query = `user_id=${userId}`;

		if (currentPage !== 0) {
			query += `&page=${currentPage}`;
		}

		if (search) {
			query += `&query=${search}`;
		}

		if (filter.languageId != '0') {
			query += `&language_id=${filter.languageId}`;
		}

		if (filter.orderBy != '0') {
			query += `&order_by=${filter.orderBy}`;
		}

		const res = await fetch(`${import.meta.env.VITE_API_URL}/texts?${query}`);
		const data = await res.json();
		if (data.texts) {
			texts = {
				currentPage: 0,
				perPage: 0,
				totalPages: 0,
				items: []
			};

			texts.currentPage = data.page;
			texts.perPage = data.per_page;
			texts.totalPages = data.total_pages;

			for (const text of data.texts) {
				const formattedText: TextType = {
					id: text.id,
					author: text.author,
					title: text.title,
					language: text.language,
					totalWords: text.total_words,
					totalKnownWords: text.total_known_words,
					imagePath: text.image_path
						? `${BASE_URL}/${text.image_path.replace(/[\\/]+/g, '/').replace(/^\/+/, '')}`
						: '/default_book.png',
					lastVisitedPage: text.last_visited_page,
					totalPages: text.total_pages
				};
				texts.items.push(formattedText);
			}
		}
	}

	onMount(async () => {
		// Carrega a pesquisa inicial
		search = $searchStore;

		// Carrega a lista de Idiomas
		const languagesRequest = await fetch(`${import.meta.env.VITE_API_URL}/languages`);
		const languages: LanguageType[] = await languagesRequest.json();
		languageOptions = languages.map((language) => {
			return { value: language.id.toString(), label: `${language.name} (${language.code})` };
		});

		loadTexts();
	});
</script>

{#snippet header()}
	<div class="header-title">
		<h1>Minha Biblioteca</h1>
		<!-- Contador dinâmico baseado nos dados -->
	</div>
	<Button size="small" onclick={() => (isShowTextModal = true)}>
		<Upload size={20} />
		Adicionar Texto
	</Button>
{/snippet}
{#snippet options()}
	<Search placeholder="Buscar por título ou autor" size="full-width" bind:value={search} />
	<Input
		placeholder="Idioma"
		fieldType="select"
		options={languageOptions}
		bind:value={filter.languageId}
	/>
	<Input
		placeholder="Data"
		fieldType="select"
		options={orderOptions}
		bind:value={filter.orderBy}
	/>
	<Button onclick={searchOnClick} style="padding: 0rem 2rem;">Buscar</Button>
	<Button onclick={clearFilters} variant='secondary' style="padding: 0rem 2rem;">Limpar filtros</Button>
{/snippet}
<main>
	<section>
		<Card {header} {options} />
		<div class="text-body">
			{#if texts}
				<TextList texts={texts.items} onDetail={handleOnDetail} />
			{/if}
		</div>
		{#if texts}
			<div class="pagination">
				<Pagination list={texts} onPageChange={handlePagination} />
			</div>
		{/if}
	</section>

	<TextModal
		isOpen={isShowTextModal}
		onClose={() => (isShowTextModal = false)}
		onSave={handleOnSave}
	/>
	{#if currentText}
		<TextModalEdit
			text={currentText}
			isOpen={isShowTextModalEdit}
			onClose={() => (isShowTextModalEdit = false)}
			onRefresh={loadTexts}
		/>
	{/if}
</main>

<style>
	main {
		display: flex;
	}

	section {
		width: 100%;
		padding: 2rem;
	}

	.text-body {
		margin-top: 1rem;
	}

	.pagination {
		margin-top: 2rem;
	}
</style>
