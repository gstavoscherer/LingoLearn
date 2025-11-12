<script lang="ts">
	import { House, LibraryBig, BookOpen, ALargeSmall, Bookmark, LogOut } from '@lucide/svelte';
	import SidebarItem from './SidebarItem.svelte';
	import type { SidebarItemType } from '$lib/types';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';

	const GROUP_REGEX = /\([^)]*\)\//g;
	let currentPage = $derived(page.route.id?.replace(GROUP_REGEX, ''));
	
	const items: SidebarItemType[] = [
		{ page: '/home', label: 'Início', icon: House },
		{ page: '/texts', label: 'Biblioteca', icon: LibraryBig },
		{ page: '/texts/[text_id]/pages/[page_number]', callback: handleOnReading, label: 'Lendo Agora', icon: BookOpen },
		{ page: '/vocabulary', label: 'Vocabulário', icon: ALargeSmall },
		{ page: '/quizzes', label: 'Quizzes', icon: Bookmark }
	];

	const footerItems: SidebarItemType[] = [
		{ page: '/login', label: 'Sair', icon: LogOut, style: 'red' }
	];

	let updatedItems = $derived(
		items.map((item) => ({
			...item,
			isActive: item.page === currentPage
		}))
	);

	let updatedFooterItems = $derived(
		footerItems.map((item) => ({
			...item,
			isActive: item.page === currentPage
		}))
	);

	async function handleOnReading() {
		const resUser = await fetch(`${import.meta.env.VITE_API_URL}/users/${page.data.user.id}`);
		const {last_visited_text_id} = await resUser.json();
		const lastTextId = last_visited_text_id;

		if (lastTextId) {
			const res = await fetch(`${import.meta.env.VITE_API_URL}/texts/${lastTextId}`);
			const text = await res.json();

			const lastVisitedPage = text.last_visited_page;
			goto(`/texts/${lastTextId}/pages/${lastVisitedPage}`);
			return;
		}
		goto('/texts');
	}
</script>

<aside class="sidebar">
	<nav>
		<div class="body">
			{#each updatedItems as item (item.label)}
				<SidebarItem
					{item}
					onClick={() => {
						if (item.callback) {
							item.callback(item);
						} else if (item.page) {
							goto(item.page);
						}
					}}
				/>
			{/each}
		</div>

		<div class="footer">
			{#each updatedFooterItems as item (item.label)}
				<SidebarItem
					{item}
					onClick={() => {
						if (item.callback) {
							item.callback(item);
						} else if (item.page) {
							goto(item.page);
						}
					}}
				/>
			{/each}
		</div>
	</nav>
</aside>

<style>
	.sidebar {
		position: relative;
		width: 260px;
		height: 100%;
		padding: 1.5rem 1rem;
		background: var(--background-white);
		display: flex;
		flex-direction: column;
		border-right: 1px solid var(--border-light);
	}

	.body {
		flex-grow: 1;
		position: relative;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.body::after {
		content: '';
		position: absolute;
		left: -1rem;
		right: -1rem;
		bottom: 0;
		height: 1px;
		background: var(--border);
	}

	nav {
		flex: 1;
		padding: 1rem 0;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 0.5rem;
	}
</style>
