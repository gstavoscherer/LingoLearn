<script lang="ts">
	import { TextCard } from '../ui';
	import type { TextType } from '$lib/types';

	interface TextListProps {
		texts: TextType[];
		onDetail: (text: TextType) => void;
	}
	let { texts, onDetail }: TextListProps = $props();

</script>

{#each texts as text (text.id)}
	<div class="wrapper">
		<TextCard {text} {onDetail} />
	</div>
{/each}

<style>
	.wrapper {
		margin-top: 1rem;
	}
</style>