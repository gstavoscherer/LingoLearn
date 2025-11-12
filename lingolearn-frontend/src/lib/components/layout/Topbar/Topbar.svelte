<script lang="ts">
	import { Search } from '$lib/components/ui';
	import Button from '$lib/components/ui/Button.svelte';
	import Logo from '$lib/components/ui/Logo.svelte';
	import { Menu, Settings } from '@lucide/svelte';
	import { goto } from '$app/navigation';
	import { searchActions } from '$lib/stores/search';

	interface TopbarProps {
		onToggleSidebar: () => void;
	}

	let {onToggleSidebar}: TopbarProps = $props();

	let search:string = $state('');

	function onSearch(event: KeyboardEvent) {
		if (event.key == "Enter") {
			searchActions.update(search);
			search = '';
			goto('/texts')
		}
	}
</script>

<header class="topbar">
	<div class="topbar-inner">
		<!-- Esquerda -->
		<div class="topbar-left">
			<div class="menu">
				<Menu onclick={onToggleSidebar} aria-label="Abrir/fechar sidebar" />
			</div>
			<a class="logo" href="/home">
				<Logo />
			</a>
		</div>

		<div class="topbar-center">
			<Search bind:value={search} placeholder="Buscar por título ou autor" onkeypress={onSearch} />
		</div>

		<!-- Direita -->
		<div class="topbar-right">
			
		</div>
	</div>
</header>

<style>
	.topbar {
		height: 88px;
		border-bottom: 1px solid var(--border-light);
		background: rgba(255, 255, 255, 0.95);
		backdrop-filter: blur(8px);
		color: #1f2937;
	}
	.menu {
		cursor: pointer;
	}
	.menu:hover {
		padding: 0.15rem 0.3rem;
		background-color: var(--background-gray);
		border-radius: 6px;
		transition: background-color 0.2s ease;
	}
	.topbar-inner {
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 100%;
		padding: 0 1.5rem; /* px-6 */
	}

	.topbar-left {
		display: flex;
		align-items: center;
		gap: 1rem;
	}
	.logo {
		cursor: default;
	}
	.topbar-center {
		flex: 1;
		max-width: 400px;
		margin: 0 2rem;
	}

	.topbar-right {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}
</style>
