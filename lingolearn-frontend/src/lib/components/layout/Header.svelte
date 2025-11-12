<script lang="ts">
	import Logo from '$lib/components/ui/Logo.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { goto } from '$app/navigation';
</script>

<header>
	<a href="/"><Logo /></a>
	<nav>
		<a class="navLink" href="/faq">FAQ</a>
		<Button variant="outline" onclick={() => goto('/login')}>Login</Button>
	</nav>
</header>

<style>
	header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem 2rem;
		background: var(--background-white);
		border-bottom: 1px solid var(--border-light);
	}

	nav {
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}

	.navLink {
		color: var(--text-secondary);
		font-weight: 500;
		transition: color 0.2s ease;
	}

	.navLink:hover {
		color: var(--primary-blue);
	}
</style>
