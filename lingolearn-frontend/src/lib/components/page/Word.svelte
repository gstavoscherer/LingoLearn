<script lang="ts">
	import type { UserWordType } from '$lib/types';
	
    interface WordProps {
        userWord: UserWordType
        onClick: (userWord: UserWordType) => void
    }    

	let {userWord, onClick}: WordProps = $props();
</script>

<div
	class="word"
	class:word-unknown={userWord.word.status === 'unknown'}
	class:word-recognize={userWord.word.status === 'recognize'}
	class:word-familiar={userWord.word.status === 'familiar'}
	class:word-well-know={userWord.word.status === 'well-known'}
	class:word-know={userWord.word.status === 'known'}
    role="button"
    tabindex="0"
    onkeydown={(e) => { if (e.key === 'Esq') onClick(userWord); }}
	onclick={() => onClick(userWord)}
	title={userWord.word.word}
>
	{userWord.word.word}
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
