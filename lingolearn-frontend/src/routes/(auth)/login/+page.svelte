<script lang="ts">
  import { enhance } from '$app/forms';
	import { page } from '$app/state';
	import { getToastState } from '$lib/toast-state.svelte.js';
  let { form } = $props();
  let loading = $state(false);

  const toastState = getToastState();

  if (page.url.searchParams.get('registered')) {
    toastState.add(
      "Conta criada!",
      "Seu cadastro foi realizado com sucesso. Bem-vindo(a) à plataforma!",
      "success"
    );
  }

</script>

<div class="auth-container">
  <div class="auth-card">
    <div class="auth-header">
      <h1>Bem-vindo de volta</h1>
      <p>Por favor, insira suas credenciais para acessar sua conta</p>
    </div>
    
    <form 
      method="POST"
      action="?/login"
      use:enhance={() => {
        loading = true;

        return async ({ update }) => {
          await update();
          loading = false;
        };
      }}
      class="auth-form"
      onsubmit={() => loading = true}
    >
      {#if form && form.success === false}
        <div class="error-message">
          {form?.error ?? 'Erro ao fazer login. Verifique suas credenciais.'}
        </div>
      {/if}

      <div class="input-group">
        <label for="email">Email</label>
        <input id="email" name="email" type="email" required placeholder="seu@email.com" />
      </div>
      
      <div class="input-group">
        <label for="password">Senha</label>
        <input id="password" name="password" type="password" required placeholder="••••••••" />
        <a href="/" class="forgot-password">Esqueceu sua senha?</a>
      </div>
      
      <button type="submit" class="auth-button" disabled={loading}>
        {#if loading}
          Entrando...
        {:else}
          Entrar
        {/if}
      </button>
    </form>
    
    <div class="signup-section">
      <p>Não tem uma conta? <a href="/register" class="signup-link">Crie uma conta</a></p>
    </div>
  </div>
</div>
