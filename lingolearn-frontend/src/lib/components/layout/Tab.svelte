<script lang="ts">
	import { Button } from '$lib/components/ui';
	import type { Snippet } from 'svelte';

	interface TabProps {
		items: {
			label: string;
			content: Snippet;
		}[];
	}

	let { items }: TabProps = $props();
	let currentActiveItem: string = $state(items[0].label);
</script>

<div class="tab">
	<div class="tab-header">
		<div class="tab-buttons">
			{#each items as item (item.label)}
				<Button
					variant={item.label === currentActiveItem ? 'primary' : 'outline'}
					size="fullWidth"
					onclick={() => (currentActiveItem = item.label)}
				>
					{item.label}
				</Button>
			{/each}
		</div>
	</div>

	<div class="tab-content">
		{#each items as item (item.label)}
			{#if item.label === currentActiveItem}
				{@render item.content()}
			{/if}
		{/each}
	</div>
</div>

<style>
	.tab {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.tab-header {
		padding: 1rem;
		border: 1px solid var(--border);
	}

	.tab-buttons {
		display: flex;
		gap: 0.5rem;
		padding: 0.5rem;
		background: var(--background-gray);
		border-radius: 1rem;
	}

	.tab-content {
		padding: 1rem;
	}
</style>
