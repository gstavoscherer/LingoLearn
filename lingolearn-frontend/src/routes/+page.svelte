<script lang="ts">
  import { goto } from '$app/navigation';
  import { Users, Trophy } from '@lucide/svelte';
  import { Button, FeatureCard } from '$lib/components/ui';
	import { Hero, Features, Cta, Faq } from '$lib/components/sections';
  import { Header, Footer } from '$lib/components/layout';
</script>

<div class="container">
  <Header/>

  <main>
    <Hero
      title="Aprenda idiomas de forma inteligente"
      subtitle="Importe textos, pratique vocabulário e acompanhe seu progresso com nossa plataforma!"  
    >
      {#snippet actions()}
        <Button
          size="large"
          onclick={() => goto('/register')}
        >
          Comece Agora
        </Button>
        <Button
          variant='outline'
          size='large'
          onclick={() => goto('/login')}
        >
          Fazer Login
        </Button>
      {/snippet}

      {#snippet illustration()}
        <FeatureCard>
          <Users size={24}/>
          <span>Textos Personalizados</span>
        </FeatureCard>
        <FeatureCard>
          <Trophy size={24}/>
          <span>Progresso Gamificado</span>
        </FeatureCard>
      {/snippet} 
    </Hero>
    <Features/>
    <Cta/>
    <Faq/>
  </main>

  <Footer/>
</div>

<style>
    .container {
        min-height: 100vh;
        background: linear-gradient(135deg, var(--background-white) 0%, var(--background-light) 100%);
    }

    main {
        padding: 4rem 2rem;
    }
</style>