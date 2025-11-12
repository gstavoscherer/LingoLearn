<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/state';
	import { Button } from '$lib/components/ui';
	import { Eye, EyeOff } from '@lucide/svelte';
	import { getToastState } from '$lib/toast-state.svelte';
	import { onMount } from 'svelte';
	import type { LanguageType, SelectOptions } from '$lib/types';
	import Input from '$lib/components/ui/Input.svelte';

	const toastState = getToastState();
	let languageOptions: SelectOptions[] | undefined = $state();

	let loading = $state(false);
	let password = $state('');
	let confirmPassword = $state('');
	let languageId: string = $state('0');
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

	onMount(async () => {
		// Carrega a lista de Idiomas
		const languagesRequest = await fetch(`${import.meta.env.VITE_API_URL}/languages`);
		const languages: LanguageType[] = await languagesRequest.json();
		languageOptions = languages.map((language) => {
			return { value: language.id.toString(), label: `${language.name} (${language.code})` };
		});
	});
</script>

<div class="container">
	<div class="card">
		<div class="header">
			<h1>Nova Conta</h1>
			<p>Por favor, insira suas credenciais para criar uma conta</p>
		</div>

		<form
			method="POST"
			action="?/register"
			use:enhance={() => {
				loading = true;

				return async ({ update }) => {
					await update();

					if (page.form?.error) {
						toastState.add('Formulário inválido', page.form.error, 'error');
					}

					loading = false;
				};
			}}
			class="form"
		>
			<Input 
				label="Usuário"
				placeholder="seu usuário"
				mandatory={true}
			/>

			<Input
				label="Email"
				placeholder="seu@email.com"
				mandatory={true}
			/>

			<Input
				label="Idioma nativo"
				placeholder="Selecione..."
				fieldType="select"
				mandatory={true}
				options={languageOptions}
				bind:value={languageId}
			/>

			<div class="input-group">
				<label for="password">Senha *</label>
				<div class="password-input-wrapper">
					<input
						id="password"
						name="password"
						type={showPassword ? 'text' : 'password'}
						required
						placeholder="sua senha"
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
				<label for="password2">Repita sua senha</label>
				<div class="password-input-wrapper">
					<input
						id="password2"
						name="password2"
						type={showConfirmPassword ? 'text' : 'password'}
						required
						placeholder="sua senha"
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
						Criando conta...
					{:else}
						Registrar
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
	.invalid {
		border-color: var(--error-red);
	}

	.input-group {
		font-weight: 600;
		gap: 0px;
	}

	.input-group label {
		color: var(--text-primary);
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
