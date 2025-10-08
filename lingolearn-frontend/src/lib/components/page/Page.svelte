<script lang="ts">
	import type { WordType, WordCategory } from '$lib/types';
	import Word from './Word.svelte';

	interface TokenType {
		category: WordCategory;
		value: string;
	}

	interface PageProps {
		content: string;
		language: string;
    onWordClick: (id?: number) => void
	}

	let { content, language, onWordClick }: PageProps = $props();

	function isWord(token: WordType | TokenType): token is WordType {
		return token.category === 'word';
	}

	const tokens: string[] = content.match(/[\w'’]+|[^\w\s]/g) || [];

	const formattedTokens = tokens.map((token: string) => {
		if (/[\w]/.test(token)) {
			const word: WordType = {
				category: 'word',
				status: 'unknown',
				original: token,
				translation: undefined,
				language
			};
			return word;
		} else {
			const t: TokenType = { category: 'punctuation', value: token };
			return t;
		}
	});
</script>

<div class="page">
	{#each formattedTokens as token, i (i)}
		{#if isWord(token)}
			<Word word={token} onClick={onWordClick} />
		{:else}
			<span class="punctuation">{token.value}</span>
		{/if}
	{/each}
</div>

<style>
	.page {
		width: 80%;
		padding: 1rem;
		background: var(--background-white);
		border-radius: 8px;
		border: 1px solid var(--border);
		line-height: 1.8; /* aumenta espaço entre linhas */
		word-break: break-word;
		text-align: justify;
		word-spacing: 0.2em;
	}

	.punctuation {
		display: inline-block;
		margin: 0 2px;
	}
</style>
