<script lang="ts">
	import type { Snippet } from "svelte";

    interface HeroProps {
        title: string
        subtitle: string
        actions: Snippet
        illustration: Snippet
    }

    let {title, subtitle, actions, illustration}: HeroProps = $props();
</script>

<section class="hero">
    <div class="heroContent">
        <h1 class="heroTitle">
            {title}
        </h1>
        <p class="heroSubtitle">
            {subtitle}
        </p>
        <div class="heroActions">
            {@render actions()}
        </div>
    </div>
    <div class="heroIllustration">
        {@render illustration()}
    </div>
</section>



<style>
    .hero {
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4rem;
        align-items: center;
    }

    .heroContent {
        max-width: 500px;
    }

    .heroTitle {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, var(--text-primary) 0%, var(--primary-blue) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .heroSubtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        line-height: 1.6;
    }

    .heroActions {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .heroIllustration {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        align-items: center;
    }
</style>