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
            Suportamos mais de 50 idiomas, incluindo inglês, espanhol, francês, alemão, italiano, português,
            japonês, chinês, coreano e muitos outros.
          </p>
        </div>
        <div class="faqItem">
          <h3 class="faqQuestion">É gratuito?</h3>
          <p class="faqAnswer">
            Sim! Oferecemos um plano gratuito robusto que permite importar até 10 textos por mês. Também temos
            planos premium com recursos avançados.
          </p>
        </div>
        <div class="faqItem">
          <h3 class="faqQuestion">Funciona offline?</h3>
          <p class="faqAnswer">
            Os textos já importados e palavras salvas ficam disponíveis offline. Para importar novos textos e
            sincronizar progresso, é necessária conexão com internet.
          </p>
        </div>
        <div class="faqItem">
          <h3 class="faqQuestion">Como o sistema de repetição espaçada funciona?</h3>
          <p class="faqAnswer">
            Baseado em algoritmos científicos, o sistema programa revisões das palavras nos momentos ideais para
            maximizar a retenção na memória de longo prazo.
          </p>
        </div>
        <div class="faqItem">
          <h3 class="faqQuestion">Posso usar meus próprios textos?</h3>
          <p class="faqAnswer">
            Absolutamente! Você pode importar qualquer texto: artigos, livros, letras de música, notícias. O
            aprendizado é mais eficaz com conteúdo que te interessa.
          </p>
        </div>
      </div>
    </div>
</section>

<style>
    .faq {
        padding: 4rem 2rem;
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
        font-weight: 600;
        margin-bottom: 1rem;
        color: var(--text-primary);
    }

    .faqAnswer {
        color: var(--text-secondary);
        line-height: 1.6;
    }
</style>