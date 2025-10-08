<script lang="ts">
    import type { ToastType } from '$lib/types';
    import { X } from '@lucide/svelte';
    import { getToastState } from '$lib/toast-state.svelte';
    
    interface ToastProps { toast: ToastType };

    let { toast }: ToastProps = $props();
    const toastState = getToastState();
</script>

<div class="toast {toast.variant}">
	<div class="toast-content">
		<strong class="toast-title">{toast.title}</strong>
		<p class="toast-message">{toast.message}</p>
	</div>
	<button class="toast-close" onclick={() => toastState.remove(toast.id)}>
		<X size={18} />
	</button>
</div>

<style>
    .toast {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.75rem;
        padding: 1rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        background: var(--background-white);
        border-left: 4px solid var(--primary-blue);
        animation: fadeIn 0.2s ease-out;
        min-width: 280px;
        max-width: 360px;
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
    }

    .toast-content {
        flex: 1;
    }

    .toast-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    .toast-message {
        font-size: 0.9rem;
        line-height: 1.1rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }

    .toast-close {
        background: none;
        border: 0;
        cursor: pointer;
        padding: .5rem;
        border-radius: 6px;
    }

    .toast-close:hover {
        transition: transform 0.2s ease;
        transform: scale(1.25);
    }

    .toast.success {
        border-left-color: var(--toast-success);
        background: var(--toast-success-bg);
    }
    .toast.info {
        border-left-color: var(--toast-info);
        background: var(--toast-info-bg);
    }
    .toast.warning {
        border-left-color: var(--toast-warning);
        background: var(--toast-warning-bg);
    }
    .toast.error {
        border-left-color: var(--toast-error);
        background: var(--toast-error-bg);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translate(-50%, -8px); }
        to { opacity: 1; transform: translate(-50%, 0); }
    }
</style>