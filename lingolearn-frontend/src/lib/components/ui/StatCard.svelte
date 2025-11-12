<script lang="ts">
	import type { Component } from "svelte";

    interface StatCardType {
        icon: Component;
        primary: string;
        secondary: string;
    }

    interface StatCardProps {
        statCard: StatCardType;
        variant?: 'primary' | 'secondary';
        iconSize?: number;
    }
    
    let { statCard, variant = 'primary', iconSize = 24 }: StatCardProps = $props();
</script>

<div class="stat-card" class:primary={variant === 'primary'} class:secondary={variant === 'secondary'}>
    <div class="icon">
        <statCard.icon size={iconSize} />
    </div>
    <div class="content">
        <div class="primary-text">
            {statCard.primary}
        </div>
        <div class="secondary-text">
            {statCard.secondary}
        </div>
    </div>
</div>

<style>
    .stat-card {
        display: flex;
        gap: 0.5rem;
    }

    /* Variant Primary */
    .stat-card.primary {
        width: 100%;
        gap: 1rem;
        border-top: 3px solid var(--primary-blue);
        background-color: var(--primary-blue-lightest);
        max-width: 250px;
        border-radius: 6px;
        padding: 0.6rem 1rem;
    }

    .stat-card.primary .icon {
        align-self: center;
        display: flex;
        justify-content: center;
        align-items: center;
        color: var(--primary-blue);
        background-color: var(--primary-blue-light);
        border: 1px solid var(--primary-blue);
        padding: 0.6rem;
        border-radius: 8px;
    }

    /* Variant Secondary */
    .stat-card.secondary .icon {
        align-self: center;
        color: var(--primary-blue);
    }

    .content {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .primary-text {
        font-weight: 700;
    }

    .secondary-text {
        color: var(--text-secondary);
    }
</style>