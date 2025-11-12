<script lang="ts">
    import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
    import { Button } from '$lib/components/ui/';
    
    let loading = $state(false);

</script>
  
<div class="container">
    <div class="card">
        <div class="header">
            <h1>Esqueceu sua senha?</h1>
            <p>Digite seu e-mail para receber o link de recuperação</p>
        </div>
        
        <form 
            method="POST"
            action="?/recover"
            use:enhance={() => {
                loading = true;

                return async ({ update }) => {
                await update();
                loading = false;
                };
            }}
            class="form"
            onsubmit={() => loading = true}
        >
            <div class="input-group">
                <label for="email">Email</label>
                <input id="email" name="email" type="email" required placeholder="seu@email.com" />
            </div>
            
            <div class="buttons">
                <Button
                    variant="secondary"
                    style="padding: 0.75rem 2.5rem;"
                    onclick={() => goto("/login")}
                >
                    Voltar
                </Button>

                <Button
                    type="submit"
                    style="padding: 0.75rem 2.5rem;"
                    disable={loading}
                >
                    {#if loading}
                        Enviando...
                    {:else}
                        Enviar
                    {/if}
                </Button>
            </div>
            
        </form>

        <div class="signup-section">
        <p>Já tem uma conta? <a href="/login" class="signup-link">Fazer Login</a></p>
        </div>
    </div>
</div>

<style>
    .buttons {
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
    }
    
</style>
  