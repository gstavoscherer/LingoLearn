<script lang="ts">
	import { getToastState } from '$lib/toast-state.svelte';
	import { Toast } from '$lib/components/ui';

	const toastState = getToastState();
</script>

<div class="toast-container">
	{#each toastState.toasts as toast, i (i)}
		<Toast {toast} />
	{/each}
</div>

<style>
.toast-container {
	position: absolute;
	top: 0.5rem;
	right: 0.5rem;
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}
</style>