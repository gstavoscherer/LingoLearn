<script lang="ts">
	import { Search } from '@lucide/svelte';

	type Size = 'medium' | 'full-width';

	interface SearchProps {
		placeholder?: string;
		size?: Size;
		value: string;
		[key: string]: unknown;
	}

	let { placeholder, size, value = $bindable(), ...rest}: SearchProps = $props();

	placeholder ??= 'Pesquisar...';
	size ??= 'medium';
</script>

<div class="search-wrapper" {...rest}>
	<div class="search-icon">
		<Search size={20} />
	</div>
	<input type="text" {placeholder} class:full-width={size === 'full-width'} bind:value={value}/>
</div>

<style>
	.search-wrapper {
		position: relative;
		display: inline-block;
		width: 100%;
	}

	.search-wrapper input {
		padding-left: 2.5rem;
		height: 40px;
		width: 100%;
		box-sizing: border-box;
		background-color: var(--background-gray);
	}

	.search-icon {
		position: absolute;
		top: 60%;
		left: 0.75rem;
		transform: translateY(-50%);
		pointer-events: none;
		color: #999;
	}

	.full-width {
		width: 100%;
	}
</style>
