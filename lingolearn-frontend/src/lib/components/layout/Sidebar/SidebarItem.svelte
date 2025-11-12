<script lang="ts">
	import type { SidebarItemType } from '$lib/types';

	interface SidebarItemProps {
		item: SidebarItemType;
		onClick: (item: SidebarItemType) => void;
	}

	let { item, onClick }: SidebarItemProps = $props();

	let isActive = $derived(item.isActive ?? false);
	let style = $derived(item.style ?? 'blue');
</script>

<button
	class="navItem"
	class:blue={style === 'blue'}
	class:red={style === 'red'}
	class:active={isActive}
	onclick={() => onClick(item)}
>
	<item.icon size={24} />
	<span>{item.label}</span>
</button>

<style>
	.navItem {
		width: 80%;
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.75rem 1rem;
		background: none;
		color: var(--text-primary);
		font-size: 1rem;
		font-weight: 600;
		transition: all 0.2s ease;
		border-left: 3px solid transparent;
	}

	.navItem.blue:hover {
		background: var(--primary-blue-light);
		color: var(--primary-blue);
		border-radius: 12px;
	}

	.navItem.red:hover {
		background: var(--error-red-light);
		color: var(--error-red);
        border-radius: 12px;
	}

	.navItem.active {
		background: var(--primary-blue-light);
		border-radius: 12px;
		color: var(--primary-blue);
		border: 1px solid #bfdbfe;
	}
</style>
