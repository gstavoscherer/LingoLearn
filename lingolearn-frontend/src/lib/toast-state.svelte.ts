import { getContext, onDestroy, setContext } from 'svelte';
import type { ToastType, ToastVariant } from './types';

export class ToastState {
	toasts = $state<ToastType[]>([]);
	toastToTimeoutMap = new Map<string, ReturnType<typeof setTimeout>>();

	constructor() {
		onDestroy(() => {
			for (const timeout of this.toastToTimeoutMap.values()) {
				clearTimeout(timeout);
			}
			this.toastToTimeoutMap.clear();
		});
	}

	add(title: string, message: string, type: ToastVariant, durationMs: number = 5000) {
		const id = crypto.randomUUID();
		this.toasts.push({
			id,
			title,
			message,
            variant: type
		});

		this.toastToTimeoutMap.set(
			id,
			setTimeout(() => {
				this.remove(id);
			}, durationMs)
		);
	}

	remove(id: string) {
		const timeout = this.toastToTimeoutMap.get(id);
		if (timeout) {
			clearTimeout(timeout);
			this.toastToTimeoutMap.delete(id);
		}
		this.toasts = this.toasts.filter((toast) => toast.id !== id);
	}
}

const TOAST_KEY = Symbol('TOAST');

export function setToastState() {
	return setContext(TOAST_KEY, new ToastState());
}

export function getToastState() {
	return getContext<ReturnType<typeof setToastState>>(TOAST_KEY);
}