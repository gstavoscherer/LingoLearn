<script lang="ts">
	import { page } from '$app/state';
	import { Toaster } from '$lib/components/ui';
	import { setToastState } from '$lib/toast-state.svelte';

	import '../styles/global.scss';
	import type { LayoutProps } from './$types';
	let { children }: LayoutProps = $props();

	const toastState = setToastState();
   
    $effect(() => {
		const flash = page.data.flash;
		if (flash) {
			toastState.add(
				flash.type === 'success' ? 'Sucesso!' : 'Aviso',
				flash.message,
				flash.type
			);
		}

        page.data.flash = null;
	});

</script>

<Toaster />

{@render children()}
