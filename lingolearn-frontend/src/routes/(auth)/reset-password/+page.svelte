<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/state';
	import { Button } from '$lib/components/ui';
	import { Eye, EyeOff } from '@lucide/svelte';
	import { getToastState } from '$lib/toast-state.svelte';
	const toastState = getToastState();

	let token = page.url.searchParams.get('token');
	
	let loading = $state(false);
	let password = $state('');
	let confirmPassword = $state('');
	let showPassword = $state(false);
	let showConfirmPassword = $state(false);

	interface PasswordValidade {
		hasMinLength: boolean;
		hasUpperCase: boolean;
		hasNumber: boolean;
		hasLowerCase: boolean;
		hasSpecialChar: boolean;
		isValid: boolean;
	}

	function validatePassword(pass: string): PasswordValidade {
		const hasMinLength = pass.length >= 8;
		const hasUpperCase = /[A-Z]/.test(pass);
		const hasLowerCase = /[a-z]/.test(pass);
		const hasNumber = /[0-9]/.test(pass);
		const hasSpecialChar = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(pass);
		return {
			hasMinLength,
			hasUpperCase,
			hasLowerCase,
			hasNumber,
			hasSpecialChar,
			isValid: hasMinLength && hasUpperCase && hasLowerCase && hasNumber && hasSpecialChar
		};
	}

	let passwordValidation = $derived(validatePassword(password));
	let passwordsMatch = $derived(password === confirmPassword && confirmPassword !== '');
	let canSubmit = $derived(passwordValidation.isValid && passwordsMatch && !loading);
</script>

<div class="container">
	<div class="card">
		<div class="header">
			<h1>Redefinir Senha</h1>
			<p>Crie uma nova senha para sua conta</p>
		</div>

		<form
			method="POST"
			action="?/reset"
			use:enhance={() => {
				loading = true;

				return async ({ update }) => {
					await update();

					if (page.form?.error) {
						toastState.add('Ocorreu um erro', page.form.error, 'error');
					}

					loading = false;
				};
			}}
			class="form"
		>
			{#if token}
				<input type="hidden" name="token" value={token} />
			{/if}
			<div class="input-group">
				<label for="password">Nova Senha</label>
				<div class="password-input-wrapper">
					<input
						id="password"
						name="password"
						type={showPassword ? 'text' : 'password'}
						required
						placeholder="sua nova senha"
						bind:value={password}
						class:invalid={password && !passwordValidation.isValid}
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
				<div class="password-requirements">
					<div
						class:valid={passwordValidation.hasMinLength}
						class:invalid={password && !passwordValidation.hasMinLength}
					>
						• Mínimo 8 caracteres
					</div>
					<div
						class:valid={passwordValidation.hasUpperCase}
						class:invalid={password && !passwordValidation.hasUpperCase}
					>
						• Pelo menos 1 letra maiúscula
					</div>
					<div
						class:valid={passwordValidation.hasLowerCase}
						class:invalid={password && !passwordValidation.hasLowerCase}
					>
						• Pelo menos 1 letra minúscula
					</div>
					<div
						class:valid={passwordValidation.hasNumber}
						class:invalid={password && !passwordValidation.hasNumber}
					>
						• Pelo menos 1 número
					</div>
					<div
						class:valid={passwordValidation.hasSpecialChar}
						class:invalid={password && !passwordValidation.hasSpecialChar}
					>
						• Pelo menos 1 caractere especial
					</div>
				</div>
			</div>

			<div class="input-group">
				<label for="password2">Confirmar Nova Senha</label>
				<div class="password-input-wrapper">
					<input
						id="password2"
						name="password2"
						type={showConfirmPassword ? 'text' : 'password'}
						required
						placeholder="confirme sua nova senha"
						bind:value={confirmPassword}
						class:invalid={confirmPassword && !passwordsMatch}
					/>
					<button
						type="button"
						class="password-toggle"
						onclick={() => (showConfirmPassword = !showConfirmPassword)}
					>
						{#if showConfirmPassword}
							<Eye size={22} />
						{:else}
							<EyeOff size={22} />
						{/if}
					</button>
				</div>
			</div>

			<div style="padding: 0rem 2rem">
				<Button
					size="fullWidth"
					style="padding: 0.75rem 2rem"
					type="submit"
					disabled={!canSubmit}
				>
					{#if loading}
						Redefinindo senha...
					{:else}
						Redefinir Senha
					{/if}
				</Button>
			</div>
		</form>

		<div class="signup-section">
			<p>Lembrou sua senha? <a href="/login" class="signup-link">Fazer Login</a></p>
		</div>
	</div>
</div>

<style>
	.invalid {
		border-color: var(--error-red);
	}

	.password-requirements {
		margin-top: 0.5rem;
		font-size: 0.8rem;
	}

	.password-requirements div {
		margin: 0.2rem 0;
	}

	.password-requirements .invalid {
		color: var(--error-red);
	}

	.password-requirements .valid {
		color: var(--success-green);
	}

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
