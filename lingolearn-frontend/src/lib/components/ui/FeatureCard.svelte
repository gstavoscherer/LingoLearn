<script lang="ts">
    let { children } = $props();
</script>

<div class="featureCard">
    {@render children()}
</div>

<style>
    .featureCard {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.5rem 2rem;
        background: var(--background-white);
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        color: var(--primary-blue);
        font-weight: 600;
        transition: transform 0.2s ease;
    }

    .featureCard:hover {
        transform: translateY(-2px);
    }
</style>
