<script lang="ts">
    import { enhance } from '$app/forms';
    let { form } = $props();
    let password = $state('');
    let password2 = $state('');
    let loading = $state(false);
  </script>
  
  <div class="auth-container">
    <div class="auth-card">
        <div class="auth-header">
            <h1>Nova Conta</h1>
            <p>Por favor, insira suas credenciais para acessar sua conta</p>
        </div>
      
        <form 
            method="POST"
            action="?/register"
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
            <div class="input-group">
                <label for="username">Usuário</label>
                <input id="username" name="username" type="text" required placeholder="seu usuário">
            </div>

            <div class="input-group">
                <label for="email">Email</label>
                <input id="email" name="email" type="email" required placeholder="seu@email.com" />
            </div>
            
            <div class="input-group">
                <label for="password">Senha</label>
                <input id="password" name="password" type="password" required placeholder="••••••••" />
            </div>

            <div class="input-group">
                <label for="password2">Repita sua senha</label>
                <input id="password2" name="password2" type="password" required placeholder="••••••••" />
            </div>
            
            <button type="submit" class="auth-button" disabled={loading}>
                {#if loading}
                    Entrando...
                {:else}
                    Registar
                {/if}
            </button>
      </form>

      <div class="signup-section">
        <p>Já tem uma conta? <a href="/login" class="signup-link">Fazer Login</a></p>
      </div>
    </div>
  </div>
  