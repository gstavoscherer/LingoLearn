<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import { goto } from '$app/navigation';

</script>

<div class="modal-overlay">
	<div class="modal-content">
		<div class="modal-icon">
			<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
				<path d="M12 8v4l3 3" stroke-width="2" stroke-linecap="round"/>
				<circle cx="12" cy="12" r="10" stroke-width="2"/>
			</svg>
		</div>
		<h2 class="modal-title">Revisões Concluídas!</h2>
		<p class="modal-message">
			Você já completou todas as revisões de hoje. <br>
		</p>
		<div class="modal-actions">
			<Button onclick={() => goto('/home')} size="large">
				Voltar para Leitura
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

	.modal-icon {
		color: var(--primary-blue);
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
		margin-bottom: 2rem;
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