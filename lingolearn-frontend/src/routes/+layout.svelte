<script lang="ts">
	import { Toaster } from '$lib/components/ui';
	import { setToastState } from '$lib/toast-state.svelte';
    import '../styles/global.scss';
    import type { LayoutProps } from './$types';
    let {children }: LayoutProps = $props();

    setToastState();
</script>

<Toaster />

{@render children()}