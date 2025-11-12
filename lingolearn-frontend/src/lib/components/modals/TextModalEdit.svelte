<script lang="ts">
	import { Button, Input } from '$lib/components/ui';
	import { getToastState } from '$lib/toast-state.svelte';
	import {
		X,
		BookOpen,
		Image as ImageIcon,
		Upload as UploadIcon,
		Trash2,
		FileText,
		Save
	} from '@lucide/svelte';
	import type { LanguageType, SelectOptions, TextType } from '$lib/types';
	import { onMount } from 'svelte';

	const toastState = getToastState();
	const BASE_URL = import.meta.env.VITE_API_URL;

	interface TextModalEditProps {
		isOpen: boolean;
		onClose: () => void;
		onRefresh: () => void;
		text: TextType;
	}

	interface EditFormType {
		title: string;
		author: string;
		language_id: string;
	}

	let { isOpen, onClose, onRefresh, text }: TextModalEditProps = $props();

	// Estado local para edição
	let editForm: EditFormType = $state({
		title: text.title,
		author: text.author,
		language_id: text.language.id.toString()
	});

	let coverInput: HTMLInputElement | undefined = $state();
	let coverFile: File | null = $state(null);
	let coverPreview: string | null = $state(text.imagePath || null);

	let languageOptions: SelectOptions[] | undefined = $state();

	onMount(async () => {
		// Carrega a lista de Idiomas
		const languagesRequest = await fetch(`${import.meta.env.VITE_API_URL}/languages`);
		const languages: LanguageType[] = await languagesRequest.json();
		languageOptions = languages.map((language) => {
			return { value: language.id.toString(), label: `${language.name} (${language.code})` };
		});
	});

	// Funções para capa
	function resetCover() {
		if (coverPreview && coverPreview.startsWith('blob:')) {
			URL.revokeObjectURL(coverPreview);
		}
		coverFile = null;
		coverPreview = text.imagePath || null;
		if (coverInput) coverInput.value = '';
	}

	function onCoverPicked(file: File) {
		if (!file?.type.startsWith('image/')) return;
		resetCover();
		coverFile = file;
		coverPreview = URL.createObjectURL(file);
	}

	function onCoverChange(e: Event) {
		const f = (e.target as HTMLInputElement).files?.[0];
		if (f) onCoverPicked(f);
	}

	function onCoverDrop(e: DragEvent) {
		e.preventDefault();
		const f = e.dataTransfer?.files?.[0];
		if (f) onCoverPicked(f);
	}

	function onCoverDragOver(e: DragEvent) {
		e.preventDefault();
	}

	// Modal functions
	function handleOnClose(event: MouseEvent) {
		if (event.target === event.currentTarget) onClose();
	}

	function handleOnKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') onClose();
	}

	// Reset form quando o texto muda
	$effect(() => {
		editForm = {
			title: text.title,
			author: text.author,
			language_id: text.language.id.toString()
		};
		coverPreview = text.imagePath || null;
		coverFile = null;
	});

	// Save function
	async function handleSave() {
		try {
			const formData = new FormData();

			// Apenas envia campos que foram modificados
			if (editForm.title !== text.title) {
				formData.append('title', editForm.title);
			}
			if (editForm.author !== text.author) {
				formData.append('author', editForm.author);
			}
			if (editForm.language_id !== text.language.id.toString()) {
				formData.append('language_id', editForm.language_id);
			}

			/* Função para salvar a capa
			if (coverFile) {
				formData.append('image', coverFile, coverFile.name);
			}
			*/

			// Se há algum campo para atualizar
			if (formData.keys().next().done && !coverFile) {
				toastState.add('Info', 'Nenhuma alteração foi feita.', 'info');
				onClose();
				return;
			}

			const response = await fetch(`${BASE_URL}/texts/${text.id}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					title: editForm.title,
					author: editForm.author,
					language_id: Number(editForm.language_id)
				})
			});

			if (!response.ok) {
				throw new Error('Erro ao atualizar texto');
			}

			toastState.add('Sucesso!', 'Texto atualizado com sucesso.', 'success');
			onRefresh();
			onClose();

			// Dispara evento para atualizar a lista
			window.dispatchEvent(new CustomEvent('textUpdated'));
		} catch (error) {
			console.error('Erro ao atualizar texto:', error);
			toastState.add('Erro', 'Não foi possível atualizar o texto.', 'error');
		}
	}

	async function handleDelete() {
		try {
			const response = await fetch(`${BASE_URL}/texts/${text.id}`, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (!response.ok) {
				throw new Error(`Erro ao deletar texto: ${response.statusText}`);
			}

			toastState.add('Sucesso', 'Texto deletado com sucesso!', 'success');
			onRefresh();
			onClose();
			return;
		} catch (error) {
			console.error('Erro ao deletar texto:', error);
			toastState.add('Erro', 'Ocorreu um erro ao deletar o texto.', 'error');
			throw error;
		}
	}

	// Cleanup effect
	$effect(() => () => {
		if (coverPreview && coverPreview.startsWith('blob:')) {
			URL.revokeObjectURL(coverPreview);
		}
	});
</script>

{#if isOpen}
	<div
		class="modal-overlay"
		onclick={handleOnClose}
		onkeydown={handleOnKeydown}
		role="dialog"
		aria-modal="true"
		aria-labelledby="modal-title"
		tabindex="0"
	>
		<div class="modal-container">
			<div class="modal-header">
				<div class="modal-title">
					<div class="modal-title-icon"><BookOpen /></div>
					<div>
						<h3 id="modal-title">Editar Texto</h3>
					</div>
				</div>
				<div class="modal-close">
					<button onclick={onClose} class="close-button" aria-label="Fechar modal"
						><X size={20} /></button
					>
				</div>
			</div>

			<div class="content-grid">
				<!-- LEFT: COVER -->
				<section class="panel">
					<h4 class="panel-title"><ImageIcon size={16} /> Capa do Texto</h4>

					<button
						type="button"
						class={'cover-drop ' + (coverPreview ? 'has-preview' : '')}
						style={coverPreview ? `background-image:url('${coverPreview}');` : ''}
						ondrop={onCoverDrop}
						ondragover={onCoverDragOver}
						onclick={() => coverInput?.click()}
						aria-label="Alterar capa do texto"
					>
						{#if !coverPreview}
							<UploadIcon size={42} />
							<p>
								Arraste e solte a nova capa aqui<br /><small
									>ou clique para selecionar</small
								>
							</p>
						{/if}
					</button>

					<div class="cover-actions">
						<input
							type="file"
							accept="image/*"
							bind:this={coverInput}
							onchange={onCoverChange}
							hidden
						/>
						{#if coverFile || coverPreview}
							<!-- Trecho para Remover a capa
							<div class="file-chip">
								<span>{coverFile ? coverFile.name : 'Capa atual'}</span>
								<button
									type="button"
									class="icon-btn"
									onclick={resetCover}
									aria-label="Restaurar capa original"
								>
									<Trash2 size={16} />
								</button>
							</div>
						-->
						{/if}
					</div>

					<!-- Informações estatísticas -->
					<div class="stats-grid">
						<div class="stat-item">
							<span class="stat-label">Páginas</span>
							<span class="stat-value">{text.lastVisitedPage}/{text.totalPages}</span>
						</div>
						<div class="stat-item">
							<span class="stat-label">Palavras</span>
							<span class="stat-value"
								>{text.totalKnownWords.toLocaleString()}/{text.totalWords.toLocaleString()}</span
							>
						</div>
						<div class="stat-item">
							<span class="stat-label">Progresso</span>
							<span class="stat-value">
								{text.totalPages > 0
									? Math.round((text.lastVisitedPage / text.totalPages) * 100)
									: 0}%
							</span>
						</div>
						<div class="stat-item">
							<span class="stat-label">Conhecimento</span>
							<span class="stat-value">
								{text.totalWords > 0
									? Math.round((text.totalKnownWords / text.totalWords) * 100)
									: 0}%
							</span>
						</div>
					</div>
				</section>

				<!-- RIGHT: DETAILS -->
				<section class="panel">
					<h4 class="panel-title"><FileText size={16} /> Informações do texto</h4>

					<div class="form-grid">
						<Input
							label="Título"
							placeholder="Digite o título do texto"
							type="text"
							mandatory={true}
							variant="fullWidth"
							bind:value={editForm.title}
						/>
						<Input
							label="Autor"
							placeholder="Digite o autor"
							type="text"
							mandatory={true}
							variant="fullWidth"
							bind:value={editForm.author}
						/>
						<Input
							label="Idioma"
							fieldType="select"
							options={languageOptions}
							placeholder="Ex.: pt-BR, en"
							type="text"
							mandatory={true}
							variant="fullWidth"
							bind:value={editForm.language_id}
						/>
					</div>

					<!-- Informações do arquivo (readonly) -->
					<div class="file-info">
						<h5>Informações do Arquivo</h5>
						<div class="info-grid">
							<div class="info-item">
								<span class="info-label">ID:</span>
								<span class="info-value">#{text.id}</span>
							</div>
							<div class="info-item">
								<span class="info-label">Total de Páginas:</span>
								<span class="info-value">{text.totalPages}</span>
							</div>
							<div class="info-item">
								<span class="info-label">Total de Palavras:</span>
								<span class="info-value">{text.totalWords.toLocaleString()}</span>
							</div>
							<div class="info-item">
								<span class="info-label">Palavras Conhecidas:</span>
								<span class="info-value"
									>{text.totalKnownWords.toLocaleString()}</span
								>
							</div>
						</div>
					</div>
				</section>
			</div>

			<div class="modal-footer">
				<div class="modal-footer-left">
					<Button onclick={handleDelete} variant="red" size="small"
						><Trash2 />Excluir</Button
					>
				</div>
				<div class="modal-footer-right">
					<Button onclick={onClose} variant="outline" size="small">Cancelar</Button>
					<Button size="small" onclick={handleSave}><Save /> Salvar Alterações</Button>
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.modal-overlay {
		position: fixed;
		inset: 0;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
	}
	.modal-container {
		background: var(--background-white);
		border-radius: 12px;
		width: min(100%, 980px);
		box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
		overflow: hidden;
	}
	.modal-header {
		border-bottom: 1px solid var(--border-light);
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 1rem 1.25rem;
	}
	.modal-title {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}
	.modal-title-icon {
		background: var(--primary-blue-light);
		color: var(--primary-blue);
		width: 40px;
		height: 40px;
		border-radius: 10px;
		display: grid;
		place-items: center;
	}
	.close-button {
		background: none;
		border: 0;
		cursor: pointer;
		padding: 0.5rem;
		border-radius: 6px;
	}
	.close-button:hover {
		background: var(--background-gray);
	}

	.content-grid {
		display: grid;
		grid-template-columns: 360px 1fr;
		gap: 1rem;
		padding: 1rem 1.25rem;
	}

	.panel {
		background: var(--background-gray);
		border: 1px solid var(--border-light);
		border-radius: 10px;
		padding: 1rem;
	}
	.panel-title {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-weight: 600;
		margin-bottom: 0.75rem;
	}

	.cover-drop {
		position: relative;
		border: 2px dashed var(--border-focus);
		border-radius: 12px;
		min-height: 280px;
		width: 100%;
		display: grid;
		place-items: center;
		padding: 1rem;
		background: linear-gradient(180deg, rgba(0, 0, 0, 0.02), transparent);
		text-align: center;
		transition: 0.2s ease;
		cursor: pointer;
		background-size: cover;
		background-position: center;
		background-repeat: no-repeat;
	}
	.cover-drop:hover {
		transform: translateY(-1px);
		box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
	}
	.cover-drop p {
		color: var(--text-secondary);
		line-height: 1.3;
	}
	.cover-actions {
		margin-top: 0.75rem;
	}

	.file-chip {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		background: var(--background-white);
		border: 1px solid var(--border);
		border-radius: 999px;
		padding: 0.35rem 0.6rem;
		font-size: 0.9rem;
	}
	.icon-btn {
		background: none;
		border: 0;
		cursor: pointer;
		display: grid;
		place-items: center;
		padding: 0.2rem;
	}

	.form-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.75rem;
		margin-bottom: 1rem;
	}

	/* Stats grid */
	.stats-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.75rem;
		margin-top: 1rem;
		padding-top: 1rem;
		border-top: 1px solid var(--border-light);
	}

	.stat-item {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.stat-label {
		font-size: 0.75rem;
		color: var(--text-secondary);
		font-weight: 500;
	}

	.stat-value {
		font-size: 0.9rem;
		font-weight: 600;
		color: var(--text-primary);
	}

	/* File info */
	.file-info {
		margin-top: 1rem;
		padding-top: 1rem;
		border-top: 1px solid var(--border-light);
	}

	.file-info h5 {
		margin: 0 0 0.75rem 0;
		font-size: 0.9rem;
		color: var(--text-secondary);
	}

	.info-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.5rem;
	}

	.info-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.25rem 0;
	}

	.info-label {
		font-size: 0.8rem;
		color: var(--text-secondary);
	}

	.info-value {
		font-size: 0.8rem;
		font-weight: 500;
		color: var(--text-primary);
	}

	.modal-footer {
		display: flex;
		justify-content: space-between;
		border-top: 1px solid var(--border-light);
	}

	.modal-footer-left,
	.modal-footer-right {
		padding: 1rem 1.25rem;

		display: flex;
		justify-content: flex-end;
		gap: 0.75rem;
	}

	@media (max-width: 860px) {
		.content-grid {
			grid-template-columns: 1fr;
		}
		.cover-drop {
			min-height: 240px;
		}
		.form-grid {
			grid-template-columns: 1fr;
		}
		.stats-grid,
		.info-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
