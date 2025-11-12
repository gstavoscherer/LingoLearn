<script lang="ts">
	import { page } from '$app/state';
	import type { WordCategory, TextPageType, UserWordType } from '$lib/types';
	import Word from './Word.svelte';

	interface TokenType {
		category: WordCategory;
		value: string;
	}

	interface PageProps {
		textPage: TextPageType;
		userWords: UserWordType[];
		onWordClick: (userWord: UserWordType) => void;
	}

	let { textPage, userWords, onWordClick }: PageProps = $props();

	function isWord(token: UserWordType | TokenType): token is UserWordType {
		return 'word' in token && token.word.category === 'word';
	}

	// Cria um mapa das palavras do usuário para acesso rápido
	const userWordsMap = $derived(
		new Map(userWords.map((userWord) => [userWord.word.word.toLowerCase(), userWord]))
	);

	let tokens = $derived(textPage.page.content.match(/[\p{L}\p{N}'’]+|[^\p{L}\p{N}\s]/gu) || []);

	const formattedTokens = $derived(
		tokens.map((token: string) => {
			if (/[\w]/.test(token)) {
				// Verifica se a palavra existe nas userWords
				const userWord = userWordsMap.get(token.toLowerCase());

				if (userWord) {
					// Usa a palavra do usuário com todas as informações
					return userWord;
				} else {
					// Cria uma WordType padrão para palavras desconhecidas
					const defaultWord: UserWordType = {
						context: getContext(textPage.page.content, token),
						easinessFactor: 1.5,
						translationLanguageId: page.data.user.translationLanguageId,
						userId: page.data.user.id,
						isNew: true,
						word: {
							id: undefined,
							word: token,
							languageId: textPage.text.language.id,
							category: 'word',
							status: 'unknown',
						}
					};
					return defaultWord;
				}
			} else {
				// Mantém a pontuação como estava
				const t: TokenType = { category: 'punctuation', value: token };
				return t;
			}
		})
	);

	function getContext(content: string, word:string): string {
		const maxSize = 100;
		if (!content || !word) return '';

		// Encontra a posição da palavra no texto (case insensitive)
		const lowerContent = content.toLowerCase();
		const lowerWord = word.toLowerCase();
		const wordIndex = lowerContent.indexOf(lowerWord);

		// Se a palavra não foi encontrada, retorna string vazia
		if (wordIndex === -1) return '';

		// Encontra o início da frase (último ponto final, quebra de linha ou início do texto)
		let start = wordIndex;
		while (start > 0) {
			const char = content[start - 1];
			if (char === '.' || char === '!' || char === '?' || char === '\n') {
				break;
			}
			start--;
		}

		// Encontra o fim da frase (próximo ponto final, quebra de linha ou fim do texto)
		let end = wordIndex + word.length;
		while (end < content.length) {
			const char = content[end];
			if (char === '.' || char === '!' || char === '?' || char === '\n') {
				end++;
				break;
			}
			end++;
		}

		// Extrai a frase completa
		let sentence = content.slice(start, end).trim();

		// Se a frase for muito longa, limita a maxSize caracteres sem cortar palavras
		if (sentence.length > maxSize) {
			// Encontra o limite de maxSize caracteres
			let limit = maxSize;

			// Volta até encontrar um espaço para não cortar palavras
			while (limit > 0 && sentence[limit] !== ' ' && sentence[limit] !== undefined) {
				limit--;
			}

			// Se encontrou um espaço, corta até lá, senão corta no maxSize
			if (limit > 0) {
				sentence = sentence.slice(0, limit) + '...';
			} else {
				sentence = sentence.slice(0, maxSize) + '...';
			}
		}

		return sentence;
	}
</script>

<div class="page">
	{#each formattedTokens as token, i (i)}
		{#if isWord(token)}
			<Word userWord={token} onClick={onWordClick} />
		{:else}
			<span class="punctuation">{token.value}</span>
		{/if}
	{/each}
</div>

<style>
	.page {
		width: 100%;
		max-height: 63vh;
		padding: 1rem;
		background: var(--background-white);
		border-radius: 8px;
		border: 1px solid var(--border);
		line-height: 1.8; /* aumenta espaço entre linhas */
		word-break: break-word;
		text-align: justify;
		word-spacing: 0.2em;
		overflow-y: auto;
	}

	.punctuation {
		display: inline-block;
		margin: 0 2px;
	}
</style>
