<script lang="ts">
	import type { UserWordType } from '$lib/types';
	import UserWordCard from './UserWordCard.svelte';

	interface UserWordListProps {
		userWords: UserWordType[];
		handleOnClick: (userWord: UserWordType) => void;
		handleDeleteOnClick: (wordId: number) => void;
	}

	let { userWords, handleOnClick, handleDeleteOnClick }: UserWordListProps = $props();
</script>

{#each userWords as userWord (userWord.word.id)}
	<UserWordCard
		{userWord}
		onClick={handleOnClick}
		deleteOnClick={handleDeleteOnClick}
	/>
{/each}

<style>
</style>
