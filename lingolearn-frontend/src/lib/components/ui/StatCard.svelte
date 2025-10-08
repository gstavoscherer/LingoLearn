<script lang="ts">
	import type { Component } from "svelte";

    interface StatCardType {
        icon: Component
        primary: string
        secondary: string
    }

    interface StatCardProps {
        statCard: StatCardType
    }
    let { statCard }: StatCardProps = $props();

</script>

<div class="stat-card">
    <div class="icon">
        <statCard.icon/>
    </div>
    <div class="content">
        <div class="primary">
            {statCard.primary}
        </div>
        <div class="secondary">
            {statCard.secondary}
        </div>
    </div>
</div>

<style>
    .stat-card {
        display: flex;
        gap: 0.5rem;
    }

    .icon {
        align-self: center;
        color: var(--primary-blue);
    }

    .content {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .primary {
        font-weight: 700;
    }
</style>