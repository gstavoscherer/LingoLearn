<script lang="ts">
	import type { Snippet } from "svelte";


    interface CardProps {
        header: Snippet;
        options: Snippet
    }

    let {header, options }: CardProps = $props();

</script>

<div class="card">
    <div class="card-header">
        <header>
            {@render header()}
        </header>
        <div class="options">
            {@render options()}
        </div>
    </div>
</div>

<style>
    header {
		width: 100%;
		display: flex;
		justify-content: space-between;
		margin-bottom: 6rem;
	}

	.card-header {
		padding: 2rem 2rem;
		background-color: var(--background-white);
		border: 1px solid var(--border);
		border-radius: 8px;
	}

	.options {
		display: flex;
		gap: 1rem;
	}
</style>