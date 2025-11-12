<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import Button from '$lib/components/ui/Button.svelte';

	let id: string;
	let name = '';
	let email = '';
	let loading = false;
	let error = '';

	// Extrai o ID da URL
	$: id = $page.params.id;

	onMount(async () => {
		try {
			const res = await fetch(`/api/users/${id}`);
			if (!res.ok) throw new Error('Erro ao carregar usuário');
			const user = await res.json();
			name = user.name;
			email = user.email;
		} catch (err) {
			error = err.message;
		}
	});

	const updateUser = async () => {
		loading = true;
		error = '';
		try {
			const res = await fetch(`/api/users/${id}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ name, email })
			});
			if (!res.ok) throw new Error('Erro ao atualizar usuário');
			await goto('/users');
		} catch (err) {
			error = err.message;
		} finally {
			loading = false;
		}
	};
</script>

<section class="max-w-xl mx-auto p-6">
	<h1 class="text-2xl font-bold mb-4">Editar Usuário</h1>

	{#if error}
		<div class="bg-red-100 text-red-800 p-2 rounded mb-4">{error}</div>
	{/if}

	<form on:submit|preventDefault={updateUser} class="space-y-4">
		<div>
			<label for="name" class="block text-sm font-medium">Nome</label>
			<input
				id="name"
				type="text"
				bind:value={name}
				class="w-full mt-1 p-2 border rounded"
				required
			/>
		</div>

		<div>
			<label for="email" class="block text-sm font-medium">Email</label>
			<input
				id="email"
				type="email"
				bind:value={email}
				class="w-full mt-1 p-2 border rounded"
				required
			/>
		</div>

		<div class="flex justify-end gap-2">
			<Button type="button" variant="ghost" on:click={() => goto('/users')}>
				Cancelar
			</Button>
			<Button type="submit" disabled={loading}>
				{#if loading}Salvando...{:else}Salvar{/if}
			</Button>
		</div>
	</form>
</section>
