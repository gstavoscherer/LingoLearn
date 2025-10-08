<script lang="ts">
	import { goto } from "$app/navigation";
	import Button from "../ui/Button.svelte";
</script>

<section class="cta">
    <div class="ctaContainer">
        <h2 class="ctaTitle">
            Pronto para começar sua jornada?
        </h2>
        <p class="ctaDescription">
            Junte-se a milhares de pessoas que já estão aprendendo idiomas de forma mais inteligente
        </p>
        <Button
            size='large'
            onclick={() => goto('/register')}
        >
            Começar Gratuitamente
        </Button>
    </div>
</section>

<style>
     .cta {
        padding: 4rem 2rem;
        background: linear-gradient(135deg, var(--background-light) 0%, var(--background-white) 100%);
    }

    .ctaContainer {
        max-width: 600px;
        margin: 0 auto;
        text-align: center;
    }

    .ctaTitle {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--text-primary);
    }

    .ctaDescription {
        font-size: 1.25rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        line-height: 1.6;
    }
</style>