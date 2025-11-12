<!-- src/routes/+layout.svelte -->
<script>
	let { children } = $props();
	import Topbar from '$lib/components/layout/Topbar/Topbar.svelte';
	import { SidebarMenu } from '$lib/components/layout/';
	import { onMount } from 'svelte';
	import { languagesStore } from '$lib/stores/languages';
	let sidebarOpen = $state(true);

	onMount(async () => {
		if ($languagesStore.languages.length === 0 && !$languagesStore.loading) {
			await languagesStore.load();
		}
	});
</script>

<div class="layout">
	<div class="topbar">
		<Topbar onToggleSidebar={() => (sidebarOpen = !sidebarOpen)} />
	</div>

	<div class="main-content">
		{#if sidebarOpen}
			<div class="sidebar">
				<SidebarMenu />
			</div>
		{/if}

		<div class="page-content">
			{@render children()}
		</div>
	</div>
</div>

<style>
	.layout {
		display: flex;
		flex-direction: column;
		height: 100vh;
		min-width: 0;
	}

	.topbar {
		flex-shrink: 0;
		width: 100%;
	}

	.main-content {
		display: flex;
		flex: 1;
		min-height: 0;
		min-width: 0;
		overflow: hidden;
	}

	.sidebar {
		flex-shrink: 0;
		background: var(--background-light);
		height: 100%;
		overflow-y: auto;
	}

	.page-content {
		flex: 1;
		min-width: 0;
		overflow: auto;
		padding: 1rem;
		background: var(--background-light);
	}

	.sidebar {
		transition: all 0.3s ease;
	}
</style>
