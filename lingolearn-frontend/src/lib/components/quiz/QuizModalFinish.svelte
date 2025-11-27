<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';

    interface QuizModalFinishProps {
        onContinue: () => Promise<void>;
    }

    let {onContinue}: QuizModalFinishProps = $props();

</script>

<div class="modal-overlay">
	<div class="modal-content">
		<div class="modal-icon celebration">
			<svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor">
				<path d="M9 12l2 2 4-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
				<path d="M12 2a10 10 0 110 20 10 10 0 010-20z" stroke-width="2"/>
			</svg>
		</div>
		<h2 class="modal-title">Parabéns! 🎉</h2>
		<p class="modal-message">
			Você completou esta revisão com sucesso!
		</p>
		<div class="modal-actions">
			<Button onclick={onContinue} size="large">
				Continuar
			</Button>
		</div>
	</div>
</div>

<style>
	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		animation: fadeIn 0.3s ease;
	}

	.modal-content {
		background: var(--background-white);
		padding: 2.5rem;
		border-radius: 16px;
		text-align: center;
		max-width: 400px;
		width: 90%;
		animation: scaleIn 0.3s ease;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
	}

	.modal-icon.celebration {
		color: var(--success-green);
		margin-bottom: 1.5rem;
	}

	.modal-title {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--text-primary);
		margin-bottom: 1rem;
	}

	.modal-message {
		color: var(--text-secondary);
		line-height: 1.5;
		margin-bottom: 1.5rem;
	}

	.modal-actions {
		display: flex;
		justify-content: center;
	}

	@keyframes fadeIn {
		from { opacity: 0; }
		to { opacity: 1; }
	}

	@keyframes scaleIn {
		from {
			opacity: 0;
			transform: scale(0.9);
		}
		to {
			opacity: 1;
			transform: scale(1);
		}
	}
</style>