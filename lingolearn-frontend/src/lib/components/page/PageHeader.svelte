<script lang="ts">
	import { goto } from '$app/navigation';
	import type { TextType } from '$lib/types';
	import { Button } from '../ui';
	import Progress from '../ui/Progress.svelte';
	import { ArrowLeft } from '@lucide/svelte';
	interface PageHeaderType {
		text: TextType;
	}

	let { text }: PageHeaderType = $props();
</script>

<div class="header">
	<div class="info">
		<Button variant="ghost" onclick={() => goto('/texts')}>
			<ArrowLeft /> Voltar
		</Button>
		<div class="details">
			<h2>{text.title}</h2>
			<div class="meta">{text.author}</div>
		</div>
	</div>

	<div class="progress-container">
		<span class="page">Página {text.lastVisitedPage} de {text.totalPages}</span>
		<Progress current={text.lastVisitedPage} total={text.totalPages} />
	</div>
</div>

<style>
	.header {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		font-family: sans-serif;
		padding: 1rem;
		border-bottom: 1px solid var(--border-light);
		background: var(--background-white);
		color: var(--text-primary);
	}

	.info {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.details {
		flex: 1;
		margin-left: 0.5rem;
	}

	.meta {
		font-size: 0.9rem;
		color: var(--text-secondary);
	}

	.progress-container {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.page {
		font-size: 0.8rem;
		color: var(--text-secondary);
		min-width: 80px;
	}
</style>
