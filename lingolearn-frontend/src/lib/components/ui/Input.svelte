<script lang="ts">
	import type { SelectOptions } from '$lib/types';
	import type { HTMLInputTypeAttribute } from 'svelte/elements';

	interface InputProps {
		label?: string;
		placeholder: string;
		value?: string;
		fieldType?: FieldType;
		options?: SelectOptions[];
		type?: HTMLInputTypeAttribute;
		mandatory?: boolean;
		variant?: Variant;
	}

	type FieldType = 'input' | 'select';
	type Variant = 'fullWidth';

	let {
		label,
		placeholder,
		value = $bindable(),
		fieldType,
		options,
		type,
		mandatory,
		variant
	}: InputProps = $props();


	label = mandatory ? `${label} *` : label;
	type ??= 'text';
	fieldType ??= 'input';

	let name = $derived.by(() => {
		if (label) {
			return label
				.trim()
				.normalize('NFD') // separa acentos
				.replace(/[\u0300-\u036f]/g, '') // remove acentos
				.replace(/\s+/g, '-') // troca espaços por hífen
				.replace(/[^a-zA-Z0-9-]/g, '') // remove tudo que não é letra, número ou hífen
				.replace(/-+$/, '') // ← remove hífens no final
				.toLowerCase();
		} else {
			return '';
		}
	});

	let error = $state('');

	function validate() {
		if (mandatory && !value?.trim()) {
			error = 'Este campo é obrigatório.';
		} else {
			error = '';
		}
	}

	let selected: string | undefined = $derived(value);

	$effect(() => {
		if (fieldType === 'select' && selected && options?.length) {
			value = selected;
		}
	});
</script>

{#if fieldType == 'input'}
	<div class="input" class:full-width={variant === 'fullWidth'}>
		<label for={name}>{label}</label>
		<input
			id={name}
			{name}
			{type}
			{placeholder}
			bind:value
			required={mandatory}
			onblur={validate}
		/>
		{#if error}
			<span class="error">{error}</span>
		{/if}
	</div>
{:else if fieldType == 'select'}
	<div class="select" class:full-width={variant === 'fullWidth'}>
		<label for={name}>
			{label}
		</label>
		<select id={name} {name} bind:value required={mandatory} onblur={validate}>
			<option value="0" disabled>
				{placeholder}
			</option>
			{#each options as option (option.value)}
				<option value={option.value}>
					{option.label}
				</option>
			{/each}
		</select>
		{#if error}
			<span class="error">{error}</span>
		{/if}
	</div>
{/if}

<style>
	.input {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.input label {
		font-size: 14px;
		font-weight: 600;
	}

	.input input {
		width: 100%;
		padding: 0.75rem 1rem;
		border: 1px solid var(--border-color, #d1d5db);
		border-radius: 6px;
		background-color: var(--bg-white, #fff);
		font-size: 0.875rem;
		color: var(--text-primary, #333);
		transition: all 0.2s ease;
		height: 2.75rem;
	}

	.input input:hover {
		border-color: var(--primary-color, #3b82f6);
	}

	.input input:focus {
		outline: none;
		border-color: var(--primary-color, #3b82f6);
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
	}

	.input.full-width {
		width: 100%;
	}

	.input .error {
		color: var(--error-red);
		font-size: 0.875rem;
	}

	.select {
		display: flex;
		flex-direction: column;
		min-width: 150px;
	}

	.select label {
		font-size: 14px;
		font-weight: 600;
	}

	.select select {
		width: 100%;
		padding: 0.625rem 0.875rem; /* Reduzido */
		border: 1px solid var(--border-color, #d1d5db);
		border-radius: 6px;
		background-color: var(--bg-white, #fff);
		font-size: 0.875rem;
		color: var(--text-primary, #333);
		cursor: pointer;
		transition: all 0.2s ease;
		appearance: none;
		background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
		background-repeat: no-repeat;
		background-position: right 0.75rem center;
		background-size: 1rem;
		height: 2.5rem; /* Reduzido */
	}

	.select select:hover {
		border-color: var(--primary-color, #3b82f6);
	}

	.select select:focus {
		outline: none;
		border-color: var(--primary-color, #3b82f6);
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
	}

	.select select:invalid {
		color: var(--text-muted, #6b7280);
	}

	.select select option {
		color: var(--text-primary, #333);
		padding: 0.5rem;
	}

	.select select option:first-child {
		color: var(--text-muted, #6b7280);
	}

	.select.full-width {
		width: 100%;
	}

	.select .error {
		color: var(--error-red);
		font-size: 0.875rem;
	}
</style>
