<script lang="ts">
 import { BookOpen, Users, Trophy } from '@lucide/svelte';
</script>

<section class="features">
    <div class="featuresContainer">
        <h2 class="featuresTitle">
            Como funciona
        </h2>
        <div class="featuresGrid">
            <div class="featureItem">
                <div class="featureIcon">
                    <BookOpen size={32} />
                </div>
                <h3 class="featureItemTitle">
                    Importe Textos
                </h3>
                <p class="featureItemDescription">
                    Cole qualquer texto no idioma que deseja aprender. Artigos, livros, notícias - você escolhe o
          conteúdo.
                </p>
            </div>
            <div class="featureItem">
                <div class="featureIcon">
                    <Users size={32} />
                </div>
                <h3 class="featureItemTitle">
                    Aprenda Vocabulário
                </h3>
                <p class="featureItemDescription">
                    Clique em palavras desconhecidas para ver traduções, definições e exemplos contextualizados.
                </p>
            </div>
            <div class="featureItem">
                <div class="featureIcon">
                    <Trophy size={32} />
                </div>
                <h3 class="featureItemTitle">
                    Pratique com Quizes
                </h3>
                <p class="featureItemDescription">
                    Sistema inteligente de repetição espaçada para fixar o vocabulário de forma eficiente.
                </p>
            </div>
        </div>
    </div>
</section>

<style>
    .features {
        padding: 4rem 2rem;
        background: var(--background-white);
    }

    .featuresContainer {
        max-width: 1200px;
        margin: 0 auto;
        text-align: center;
    }

    .featuresTitle {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 3rem;
        color: var(--text-primary);
    }

    .featuresGrid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
    }

    .featureItem {
        padding: 2rem;
        border-radius: 12px;
        transition: transform 0.2s ease;
    }

    .featureItem:hover {
        transform: translateY(-4px);
    }

    .featureIcon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 80px;
        height: 80px;
        background: var(--primary-blue-light);
        color: var(--primary-blue);
        border-radius: 50%;
        margin-bottom: 1.5rem;
    }

    .featureItemTitle {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: var(--text-primary);
    }

    .featureItemDescription {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 1.1rem;
    }
</style>