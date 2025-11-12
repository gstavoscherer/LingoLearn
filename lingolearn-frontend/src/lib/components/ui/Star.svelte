<script lang="ts">
	import { Star } from '@lucide/svelte';

	interface StarProps {
		rating: number;
		maxStars?: number;
		onRatingChange?: (rating: number) => void;
		size?: number;
		interactive?: boolean;
	}

	let {
		rating = $bindable(),
		maxStars = 5,
		size = 20,
		interactive = false
	}: StarProps = $props();

	let hoverRating = $state(0);

	function handleStarClick(starIndex: number) {
		if (interactive) {
			rating = starIndex + 1;
		}
	}

	function handleStarHover(starIndex: number) {
		if (interactive) {
			hoverRating = starIndex + 1;
		}
	}

	function handleMouseLeave() {
		if (interactive) {
			hoverRating = 0;
		}
	}
</script>

<div 
	class="stars-container" 
	class:interactive 
	onmouseleave={handleMouseLeave}
	role={interactive ? "slider" : "img"}
	aria-label={interactive ? "Avaliar familiaridade" : "Nível de familiaridade"}
	aria-valuenow={rating}
	aria-valuemin={0}
	aria-valuemax={maxStars}
>
	{#each Array(maxStars) as _, index(index)}
		<button
			class="star-button"
			class:filled={index < (hoverRating || rating)}
			onclick={() => handleStarClick(index)}
			onmouseenter={() => handleStarHover(index)}
			disabled={!interactive}
			aria-label={`Avaliar com ${index + 1} estrela${index + 1 === 1 ? '' : 's'}`}
			type="button"
			aria-pressed={index < rating}
		>
			<Star {size} />
		</button>
	{/each}
</div>

<style>
	.stars-container {
		display: flex;
		gap: 0.25rem;
		align-items: center;
	}

	.star-button {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0.125rem;
		background: none;
		border: none;
		cursor: pointer;
		transition: transform 0.1s ease;
		color: #d1d5db;
	}

	.star-button.filled {
		color: #fbbf24;
		fill: #fbbf24;
	}

	.star-button:disabled {
		cursor: default;
	}

	.stars-container.interactive .star-button:not(:disabled):hover {
		transform: scale(1.1);
	}

	.star-button:focus-visible {
		outline: 2px solid #3b82f6;
		outline-offset: 2px;
		border-radius: 2px;
	}
</style>