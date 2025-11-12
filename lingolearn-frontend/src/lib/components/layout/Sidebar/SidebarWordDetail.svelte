<script lang="ts">
	import { Button } from '$lib/components/ui';
	import { Star } from '$lib/components/ui/';
	import type { UserWordType } from '$lib/types';
	import { EasinnessFactorToStarRating, starRatingToLabel } from '$lib/utils';
	import { X, Volume2 } from '@lucide/svelte';
	import { onMount } from 'svelte';

	type SidebarDirection = 'left' | 'right';

	interface SidebarDetailProps {
		userWord: UserWordType;
		direction?: SidebarDirection;
		isEdit?: boolean;
		onToggle: () => void;
		saveOnClick: (starRating: number, isNew: boolean) => void;
		isOpen: boolean;
	}

	let {
		direction = 'right',
		onToggle,
		isEdit = false,
		saveOnClick,
		userWord = $bindable(),
		isOpen = $bindable()
	}: SidebarDetailProps = $props();

	let starRating: number = $state(EasinnessFactorToStarRating(userWord.easinessFactor));
	let starRatingText: string = $derived(starRatingToLabel(starRating));

	onMount(() => {
		loadData();

		document.addEventListener('keydown', handleKeydown);
		return () => {
			document.removeEventListener('keydown', handleKeydown);
		};
	});

	// Fechar ao clicar fora da sidebar
	function handleClickOutside(event: MouseEvent) {
		const overlay = document.querySelector('.overlay') as HTMLElement;

		// Se clicou diretamente no overlay (fora do sidebar)
		if (event.target === overlay) {
			onToggle();
		}
	}

	// Fechar com a tecla ESC
	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape' && isOpen) {
			onToggle();
		}
	}

	async function translate(
		text: string,
		fromLanguageId: number,
		toLanguageId: number
	): Promise<string> {
		const query = `word=${text}&src_language_id=${fromLanguageId}&dest_language_id=${toLanguageId}`;

		const response = await fetch(`${import.meta.env.VITE_API_URL}/translate?${query}`, {
			method: 'GET'
		});

		const data = await response.json();
		if (data.translation) {
			return data.translation;
		} else {
			return '';
		}
	}

	async function loadData() {
		// Busca o id da palavra
		if (!userWord.word.id) {
			const response = await fetch(`${import.meta.env.VITE_API_URL}/words?word=${userWord.word.word}&language_id=${userWord.word.languageId}`);
			const responseJson = await response.json();
			userWord.word.id = responseJson.id;
		}

		// Busca a tradução da palavra
		if (!userWord.translation) {
			userWord.translation = await translate(
				userWord.word.word,
				userWord.word.languageId,
				userWord.translationLanguageId
			);
		}

		// Busca a tradução do contexto
		if (!userWord.contextTranslation) {
			userWord.contextTranslation = await translate(
				userWord.context,
				userWord.word.languageId,
				userWord.translationLanguageId
			);
		}
	}
</script>

<div
	class:overlay={isOpen}
	class:overlay-hidden={!isOpen}
	onclick={handleClickOutside}
	role="button"
	onkeypress={handleKeydown}
	tabindex="0"
>
	<div
		class="sidebar"
		class:sidebar-right={direction === 'right'}
		class:sidebar-left={direction === 'left'}
	>
		<!-- Header -->
		<div class="sidebar-header">
			<div class="header-content">
				<h2 class="word-title">{userWord.word.word}</h2>
				<Button
					variant="ghost"
					size="small"
					onclick={onToggle}
					class="close-btn"
					aria-label="Fechar sidebar"
				>
					<X size={18} />
				</Button>
			</div>
		</div>

		<!-- Content Area -->
		<div class="sidebar-content">
			<!-- Palavra com botão de volume -->
			<div class="word-section">
				<div class="word-with-audio">
					<span class="word-text">{userWord.word.word}</span>
					<Button
						variant="secondary"
						size="small"
						class="audio-btn"
						aria-label="Ouvir pronúncia"
						style="padding: 0.5rem 0.5rem; background-color: var(--primary-blue-light); border: none;"
					>
						<Volume2 size={20} />
					</Button>
				</div>
			</div>

			<!-- Tradução -->
			{#if userWord.translation}
				<div class="content-section card">
					<h3 class="section-title">Tradução</h3>
					<p class="section-content">{userWord.translation}</p>
				</div>
			{/if}

			<!-- Contexto -->
			<div class="content-section card">
				<h3 class="section-title">Contexto</h3>
				<p class="section-content">{userWord.context}</p>
				{#if userWord.contextTranslation}
					<p>{userWord.contextTranslation}</p>
				{/if}
			</div>

			<!-- Familiaridade -->
			<div class="content-section">
				<h3 class="section-title">Familiaridade</h3>
				<Star bind:rating={starRating} interactive={isEdit} />
				<p class="section-content">{starRatingText}</p>
			</div>
		</div>

		<!-- Footer -->
		<div class="sidebar-footer">
			<Button variant="outline" size="medium" onclick={onToggle}>Fechar</Button>
			<Button variant="primary" size="medium" onclick={() => saveOnClick(starRating, userWord.isNew)}>Salvar</Button>
		</div>
	</div>
</div>

<style>
	/* Overlay */
	.overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: flex-end;
		align-items: center;
		z-index: 1000;
		animation: fadeIn 0.2s ease-out;
	}

	.overlay-hidden {
		display: none;
	}

	/* Sidebar */
	.sidebar {
		background-color: white;
		width: 350px;
		height: 100vh;
		display: flex;
		flex-direction: column;
		box-shadow: -2px 0 20px rgba(0, 0, 0, 0.1);
		transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		position: relative;
	}

	.sidebar-right {
		transform: translateX(0);
	}

	.sidebar-left {
		transform: translateX(0);
		margin-right: auto;
		box-shadow: 2px 0 20px var(--border);
	}

	/* Header */
	.sidebar-header {
		padding: 1rem 1.5rem;
		border-bottom: 1px solid #e5e7eb;
	}

	.header-content {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.word-title {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--primary-blue);
		text-transform: capitalize;
		margin: 0;
	}

	/* Content Area */
	.sidebar-content {
		flex: 1;
		padding: 1.5rem;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	/* Word Section */
	.word-section {
		margin-bottom: 0.5rem;
	}

	.word-with-audio {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.word-text {
		font-size: 1.25rem;
		text-transform: capitalize;
		font-weight: 500;
		color: var(--text-secondary);
	}

	/* Content Sections */
	.content-section {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.card p:first-of-type {
		color: var(--text-primary);
		line-height: 1.4rem;
		background-color: var(--primary-blue-light);
		padding: 1rem;
		border-left: 2px solid var(--primary-blue);
		border-radius: 8px;
	}

	.card p:nth-of-type(2) {
		color: var(--text-primary);
		line-height: 1.4rem;
		background-color: var(--primary-blue-lightest);
		padding: 1rem;
		border-left: 2px solid var(--primary-blue);
		border-radius: 8px;
	}

	.section-title {
		font-size: 0.875rem;
		font-weight: 600;
		color: #6b7280;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin: 0;
	}

	.section-content {
		font-size: 1rem;
		color: #374151;
		line-height: 1.5;
		margin: 0;
	}

	/* Footer */
	.sidebar-footer {
		display: flex;
		gap: 0.75rem;
		justify-content: flex-end;
		padding: 1.5rem;
		border-top: 1px solid #e5e7eb;
		background-color: #fafafa;
	}

	/* Animations */
	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
</style>
