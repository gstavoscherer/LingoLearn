<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/state';
	import { getToastState } from '$lib/toast-state.svelte.js';
	import { Eye, EyeOff } from '@lucide/svelte';

	let showPassword = $state(false);
	let loading = $state(false);

	const toastState = getToastState();
</script>

<div class="container">
	<div class="card">
		<div class="header">
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

					// Caso sucesso no form retorna mais cedo
					if (page.status == 303 || page.status == 200) {
						return;
					}

					// Caso erro no form adiciona toast de erro
					if (!page.form?.success) {
						toastState.add('Login inválido', 'Usuário ou senha incorretos', 'error');
					}
				};
			}}
			class="form"
			onsubmit={() => (loading = true)}
		>
			<div class="input-group">
				<label for="email">Email</label>
				<input id="email" name="email" type="email" required placeholder="seu@email.com" />
			</div>

			<div class="input-group">
				<label for="password">Senha</label>
				<div class="password-input-wrapper">
					<input
						id="password"
						name="password"
						type={showPassword ? 'text' : 'password'}
						required
						placeholder="sua senha"
					/>
					<button
						type="button"
						class="password-toggle"
						onclick={() => (showPassword = !showPassword)}
					>
						{#if showPassword}
							<Eye size={22} />
						{:else}
							<EyeOff size={22} />
						{/if}
					</button>
				</div>
				<a href="/forgot-password" class="forgot-password">Esqueceu sua senha?</a>
			</div>

			<button type="submit" class="button" disabled={loading}>
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

<style>
	.password-input-wrapper {
		position: relative;
	}

	.password-input-wrapper input {
		width: 100%;
		padding-right: 2.5rem;
	}

	.password-toggle {
		position: absolute;
		right: 0.75rem;
		top: 50%;
		transform: translateY(-50%);
		background: none;
		border: none;
		color: var(--text-primary);
		cursor: pointer;
		padding: 0.25rem;
		border-radius: 4px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
