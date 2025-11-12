<script lang="ts">
	import type { UserWordType } from '$lib/types';
	import { Trash2 } from '@lucide/svelte';
	import { Star } from '../ui/';
	import { EasinnessFactorToStarRating } from '$lib/utils';
	import Button from '../ui/Button.svelte';
	import { languagesStore } from '$lib/stores/languages';
	import { onMount } from 'svelte';

	interface UserWordCardProps {
		userWord: UserWordType;
		onClick: (userWord: UserWordType) => void;
		deleteOnClick: (wordId: number) => void;
	}

	let { userWord, onClick, deleteOnClick }: UserWordCardProps = $props();
	let rating = $derived(EasinnessFactorToStarRating(userWord.easinessFactor));
    const ellipsisLen = 25;

	onMount(async () => {
		if (!$languagesStore) {
		await languagesStore.load();
	}
	})

	let language = $derived($languagesStore.languages.filter((l) => l.id == userWord.word.languageId)[0]);
</script>

<div class="word-card" onclick={() => onClick(userWord)} role="presentation">
	<!-- Header do Card -->
	<div class="card-header">
		<div class="header-left">
			<h3 class="word-title">{userWord.word.word}</h3>
			<span class="tag">{language?.name}</span>
		</div>
		<Button
			variant="red"
			size="small"
			class="close-btn"
			aria-label="Fechar sidebar"
			style="padding: 0.4rem"
			onclick={(e: Event) => {
				e.stopPropagation();
				deleteOnClick(userWord.word.id!);
			}}
		>
			<Trash2 size={18} />
		</Button>
	</div>

	<!-- Body do Card -->
	<div class="card-body">
		{#if userWord.translation}
			<div class="content-section">
				<p class="card"><i>{userWord.translation}</i></p>
			</div>
		{/if}

		{#if userWord.context}
			<div class="content-section">
				<p style="font-size: 16px;">Contexto:</p>
				<p class="value ellipsis context-card" title={userWord.context}>
					{userWord.context.slice(
						0,
						ellipsisLen
					)}{#if userWord.context.length > ellipsisLen}...{/if}
				</p>
			</div>
		{/if}

		{#if userWord.contextTranslation}
			<div class="content-section">
				<p class="value ellipsis context-card-light" title={userWord.contextTranslation}>
					{userWord.contextTranslation.slice(
						0,
						ellipsisLen
					)}{#if userWord.contextTranslation.length > ellipsisLen}...{/if}
				</p>
			</div>
		{/if}
	</div>

	<!-- Footer do Card -->
	<div class="card-footer">
		<Star {rating} />
	</div>
</div>

<style>
	.word-card {
		background: white;
		border: 1px solid var(--border-color, #e1e5e9);
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		overflow: hidden;
		display: flex;
		flex-direction: column;
		transition:
			transform 0.2s ease,
			box-shadow 0.2s ease;
	}

	.word-card:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		cursor: pointer;
	}

	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem 1.25rem;
		background-color: var(--primary-blue-lightest, #f8fafc);
		border-bottom: 1px solid var(--border-color, #e1e5e9);
	}

	.header-left {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1rem;
	}

	.tag {
		display: inline-block;
		background: var(--primary-blue-light);
		color: var(--primary-blue);
		padding: 0.15rem 0.75rem;
		border-radius: 16px;
		font-size: 0.75rem;
		font-weight: 500;
		border: 1px solid var(--primary-blue);
		margin-top: 0.4rem;
	}

	.word-title {
		margin: 0;
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--primary-blue);
		text-transform: capitalize;
	}

	.card-body {
		padding: 1.25rem;
		flex-grow: 1;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.content-section {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.card {
		color: var(--text-primary);
		line-height: 1.4rem;
		background-color: var(--primary-blue-light);
		padding: 1rem;
		border-left: 2px solid var(--primary-blue);
		border-radius: 8px;
		text-align: center;
		font-weight: 500;
		text-transform: capitalize;
	}

	.context-card {
		color: var(--text-primary);
		line-height: 1.4rem;
		background-color: var(--primary-blue-light);
		padding: 1rem;
		border-left: 2px solid var(--primary-blue);
		border-radius: 8px;
		font-weight: 500;
	}

	.context-card-light {
		color: var(--text-primary);
		line-height: 1.4rem;
		background-color: var(--primary-blue-lightest);
		padding: 1rem;
		border-left: 2px solid var(--primary-blue);
		border-radius: 8px;
	}

	.content-section p:not(.card) {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--text-secondary, #718096);
		letter-spacing: 0.5px;
	}

	.ellipsis {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.card-footer {
		padding: 1rem 1.25rem;
		border-top: 1px solid var(--border-color, #e1e5e9);
		background-color: var(--background-secondary, #f7fafc);
		display: flex;
		justify-content: center;
	}
</style>
