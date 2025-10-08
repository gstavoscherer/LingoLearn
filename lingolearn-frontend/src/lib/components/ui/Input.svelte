<script lang="ts">
	import type { HTMLInputTypeAttribute } from "svelte/elements";
    
    interface InputProps {
        label: string
        placeholder: string
		value: string
        type?: HTMLInputTypeAttribute
        mandatory?: boolean
        variant?: Variant
    }

    type Variant = 'fullWidth';

    let { label, placeholder, type, mandatory, variant, value = $bindable() }: InputProps = $props();
    label = mandatory ? `${label} *` : label;
	type ??= "text";

    let name = $derived(
        label
            .normalize("NFD")               // separa acentos
            .replace(/[\u0300-\u036f]/g, "") // remove acentos
            .replace(/\s+/g, "-")            // troca espaços por hífen
            .replace(/[^a-zA-Z0-9-]/g, "")   // remove tudo que não é letra, número ou hífen
            .toLowerCase()
    );


	let error = $state("");

    function validate() {
		if (mandatory && !value.trim()) {
			error = "Este campo é obrigatório.";
		} else {
			error = "";
		}
	}

</script>

<div 
    class="input"
    class:full-width={variant === 'fullWidth'}
>
	<label for={name}>{label}</label>
	<input
		id={name}
		name={name}
		{type}
		{placeholder}
		bind:value
		required={mandatory}
		onblur={validate}
        
	>
	{#if error}
		<span class="error">{error}</span>
	{/if}
</div>

<style>
    label {
        font-size: 14px;
        font-weight: 600;
    }
	.input {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

    .full-width {
        width: 100%;
    }

	.error {
		color: var(--error-red);
		font-size: 0.875rem;
	}
</style>