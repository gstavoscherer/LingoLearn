<script lang="ts">
	import type { WordType } from '$lib/types';
	
    interface WordProps {
        word: WordType
        onClick: (id?: number) => void
    }    

	let {word, onClick}: WordProps = $props();

</script>

<div
	class="word"
	class:word-unknown={word.status === 'unknown'}
	class:word-recognize={word.status === 'recognize'}
	class:word-familiar={word.status === 'familiar'}
	class:word-well-know={word.status === 'well-know'}
	class:word-know={word.status === 'know'}
    role="button"
    tabindex="0"
    onkeydown={(e) => { if (e.key === 'Esq') onClick(word?.id); }}
	onclick={() => onClick(word?.id)}
	title={word.translation || word.original}
>
	{word.original}
</div>

<style>
	.word {
		display: inline-block;
		margin: 4px 2px;
		padding: 4px 6px;
		border-radius: 6px;
		cursor: pointer;
		transition:
			all 0.2s ease,
			box-shadow 0.3s ease;
		font-weight: 500;
		vertical-align: middle;
	}

	.word:hover {
		transform: translateY(-2px);
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
	}

	/* Destaques progressivos */
	.word-unknown {
		background-color: var(--toast-error-bg);
		color: var(--toast-error);
		font-weight: bold;
	}

	.word-recognize {
		background-color: var(--toast-warning-bg);
		color: var(--toast-warning);
		font-weight: 600;
	}

	.word-familiar {
		background-color: var(--toast-info-bg);
		color: var(--toast-info);
		font-weight: 500;
	}

	.word-well-know {
		background-color: var(--primary-blue-light);
		color: var(--primary-blue);
		font-weight: 500;
		opacity: 0.8;
	}

	.word-know {
		background-color: transparent;
		color: var(--text-primary);
		font-weight: normal;
		opacity: 0.6;
	}
</style>
