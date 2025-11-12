<script lang="ts">

</script>

<section id="faq" class="faq">
    <div class="faqContainer">
      <h2 class="faqTitle">Perguntas Frequentes</h2>
      <div class="faqGrid">
        <div class="faqItem">
          <h3 class="faqQuestion">Como funciona o sistema de aprendizado?</h3>
          <p class="faqAnswer">
            Você importa textos no idioma que deseja aprender, clica em palavras desconhecidas para ver traduções
            e pratica com nosso sistema de quizes baseado em repetição espaçada.
          </p>
        </div>
        <div class="faqItem">
          <h3 class="faqQuestion">Quais idiomas são suportados?</h3>
          <p class="faqAnswer">
            Atualmente, a plataforma oferece suporte a dois idiomas, permitindo que os usuários aprendam e pratiquem tanto inglês quanto espanhol de maneira integrada e eficiente.
          </p>
        </div>
        <div class="faqItem">
          <h3 class="faqQuestion">Como começar a usar o LingoLearn?</h3>
          <p class="faqAnswer">
            Crie sua conta, escolha o idioma que deseja aprender (inglês ou espanhol) e importe os textos que quiser. Depois, clique nas palavras que não conhece e pratique com nossos quizzes.
          </p>
        </div>
        <div class="faqItem">
          <h3 class="faqQuestion">É possível acompanhar meu progresso?</h3>
          <p class="faqAnswer">
            Sim. O LingoLearn registra seu avanço por texto e por palavra, permitindo que você veja claramente o que já aprendeu e o que precisa reforçar.
          </p>
        </div>
        <div class="faqItem">
          <h3 class="faqQuestion">Como o sistema de repetição espaçada funciona?</h3>
          <p class="faqAnswer">
            Baseado em algoritmos científicos, o sistema programa revisões das palavras nos momentos ideais para maximizar a retenção na memória de longo prazo.
          </p>
        </div>
        <div class="faqItem">
          <h3 class="faqQuestion">O LingoLearn oferece ajuda com pronúncia?</h3>
          <p class="faqAnswer">
            Sim. Você pode ouvir a pronúncia de palavras e frases diretamente na plataforma, o que ajuda na memorização e na prática da fala.
          </p>
        </div>
      </div>
    </div>
</section>

<style>
    .faq {
        padding: 2rem 2rem;
        background: var(--background-white);
    }

    .faqContainer {
        max-width: 1000px;
        margin: 0 auto;
    }

    .faqTitle {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 3rem;
        color: var(--text-primary);
    }

    .faqGrid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
        gap: 2rem;
    }

    .faqItem {
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-light);
        transition: all 0.2s ease;
    }

    .faqItem:hover {
        border-color: var(--primary-blue);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }

    .faqQuestion {
        font-size: 1.25rem;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1rem;
        color: var(--text-primary);
    }

    .faqAnswer {
      text-align: center;
        color: var(--text-secondary);
        line-height: 1.6;
    }
</style>