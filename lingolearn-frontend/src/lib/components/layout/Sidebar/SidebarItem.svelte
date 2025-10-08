<script lang="ts">
	import { goto } from '$app/navigation';
	import type { SidebarItemType } from '$lib/types';
    
    interface SidebarItemProps {
        item: SidebarItemType
    }
    
    let { item }: SidebarItemProps = $props();

    item.isActive ??= false;
    item.style ??= 'blue';
</script>

<button
    class="navItem"
    class:blue={item.style === 'blue'}
    class:red={item.style === 'red'}
    class:active={item.isActive}
    onclick={() => goto(item.page)}
>
    <item.icon size={24} />
    <span>{item.label}</span>
</button>

<style>
    .navItem {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1.5rem;
        background: none;
        color: var(--text-secondary);
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
        border-left: 3px solid transparent;
    }

    .navItem.blue:hover {
        background: var(--primary-blue-light);
        color: var(--primary-blue);
    }

    
    .navItem.red:hover {
        background: var(--error-red-light);
        color: var(--error-red);
    }

    .navItem.active {
    background: var(--primary-blue-light);
    color: var(--primary-blue);
    border-left-width: 6px;
    border-left-color: var(--primary-blue);
    }
</style>