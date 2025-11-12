<script lang="ts">
	import { page } from '$app/state';
	import { Button, Input } from '$lib/components/ui';
	import { getToastState } from '$lib/toast-state.svelte';
	import type { LanguageType, SelectOptions } from '$lib/types';
	import { extractTextFromEPUB, extractTextFromPDF } from '$lib/utils';
	import {
		X,
		BookOpen,
		Image as ImageIcon,
		Upload as UploadIcon,
		Trash2,
		FileText
	} from '@lucide/svelte';
	import { onMount } from 'svelte';

	const toastState = getToastState();

	interface BookFormData {
		title: string;
		author: string;
		languageId: string;
		content: string;
		user_id: string;
	}
	interface BookModalProps {
		isOpen: boolean;
		onClose: () => void;
		onSave: () => void;
	}

	let { isOpen, onClose, onSave }: BookModalProps = $props();

	let bookForm: BookFormData = $state({
		author: '',
		content: '',
		languageId: '0',
		title: '',
		user_id: page.data.user.id
	});

	let coverInput: HTMLInputElement | undefined = $state();
	let coverFile: File | null = $state(null);
	let coverPreview: string | null = $state(null);

	let textInput: HTMLInputElement | undefined = $state();
	let textFile: File | null = $state(null);
	let textFileName: string = $state('');

	let languageOptions: SelectOptions[] | undefined = $state();

	onMount(async () => {
		const languagesRequest = await fetch(`${import.meta.env.VITE_API_URL}/languages`);
		const languages: LanguageType[] = await languagesRequest.json();
		languageOptions = languages.map((language) => {
			return { value: language.id.toString(), label: `${language.name} (${language.code})` };
		});
	});

	function resetCover() {
		if (coverPreview) URL.revokeObjectURL(coverPreview);
		coverFile = null;
		coverPreview = null;
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

	// ---- text handlers
	async function onTextFileChange(e: Event) {
		const f = (e.target as HTMLInputElement).files?.[0];
		if (!f) return;
		textFileName = f.name;

		const isTxt = f.type.startsWith('text/') || /\.txt$/i.test(f.name);
		const isPdf = /pdf$/i.test(f.type) || /\.pdf$/i.test(f.name);
		const isEpub = /\.epub$/i.test(f.name);

		if (isTxt || isPdf || isEpub) textFile = null;

		if (isTxt) {
			bookForm.content = await f.text();
		} else if (isPdf) {
			bookForm.content = await extractTextFromPDF(f);
		} else if (isEpub) {
			bookForm.content = await extractTextFromEPUB(f);
		}
	}

	async function onTextDrop(e: DragEvent) {
		e.preventDefault();
		const f = e.dataTransfer?.files?.[0];
		if (!f) return;
		const dt = new DataTransfer();
		dt.items.add(f);
		if (textInput) textInput.files = dt.files;
		await onTextFileChange(new Event('change'));
	}
	function onTextDragOver(e: DragEvent) {
		e.preventDefault();
	}

	// modal
	function handleOnClose(event: MouseEvent) {
		if (event.target === event.currentTarget) onClose();
	}
	function handleOnKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') onClose();
	}

	// save
	async function handleSave() {
		const BASE_URL = import.meta.env.VITE_API_URL;
		const form = new FormData();
		form.append('title', bookForm.title || '');
		form.append('author', bookForm.author || '');
		form.append('language_id', bookForm.languageId || '');
		form.append('user_id', bookForm.user_id || '');
		form.append('content', bookForm.content || '');

		if (coverFile) form.append('image', coverFile, coverFile.name);
		if (textFile) form.append('text_file', textFile, textFile.name);

		const missingFields: string[] = [];

		if (!bookForm.title) missingFields.push('Título');
		if (!bookForm.author) missingFields.push('Autor');
		if (!bookForm.content) missingFields.push('Conteúdo');
		if (bookForm.languageId == '0') missingFields.push('Idioma');

		if (missingFields.length > 0) {
			toastState.add(
				'Erro no envio',
				`Por favor preencha os seguintes campos: ${missingFields.join(', ')}`,
				'error'
			);
			return;
		}

		await fetch(`${BASE_URL}/texts`, { method: 'POST', body: form });

		toastState.add('Sucesso!', 'Seu texto foi salvo com sucesso.', 'success');
		resetForm();
		onClose();
		onSave();
	}

	$effect(() => () => {
		if (coverPreview) URL.revokeObjectURL(coverPreview);
	});

	function resetForm() {
		bookForm = {
			author: '',
			content: '',
			languageId: '0',
			title: '',
			user_id: page.data.user.id
		};
		textFile = null;
		textFileName = '';
	}
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
						<h3 id="modal-title">Adicionar Novo Texto</h3>
						<p>Envie a capa e o conteúdo. Informe o idioma no campo abaixo.</p>
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
					<h4 class="panel-title"><ImageIcon size={16} /> Capa do texto</h4>

					<button
						type="button"
						class={'cover-drop ' + (coverPreview ? 'has-preview' : '')}
						style={coverPreview ? `background-image:url('${coverPreview}');` : ''}
						ondrop={onCoverDrop}
						ondragover={onCoverDragOver}
						onclick={() => coverInput?.click()}
						aria-label="Enviar capa do texto"
					>
						{#if !coverPreview}
							<UploadIcon size={42} />
							<p>
								Arraste e solte a capa aqui<br /><small
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
						{#if coverFile}
							<div class="file-chip">
								<span>{coverFile.name}</span>
								<button
									type="button"
									class="icon-btn"
									onclick={resetCover}
									aria-label="Remover capa"
								>
									<Trash2 size={16} />
								</button>
							</div>
						{/if}
					</div>
				</section>

				<!-- RIGHT: DETAILS + TEXT -->
				<section class="panel">
					<h4 class="panel-title"><FileText size={16} /> Informações e conteúdo</h4>

					<div class="form-grid">
						<Input
							label="Título"
							placeholder="Digite o título do texto"
							type="text"
							mandatory={true}
							variant="fullWidth"
							bind:value={bookForm.title}
						/>
						<Input
							label="Autor"
							placeholder="Digite o autor"
							type="text"
							mandatory={true}
							variant="fullWidth"
							bind:value={bookForm.author}
						/>
						<Input
							label="Idioma"
							placeholder="Idioma"
							fieldType="select"
							options={languageOptions}
							mandatory={true}
							variant="fullWidth"
							bind:value={bookForm.languageId}
						/>
					</div>

					<div class="text-upload">
						<button
							type="button"
							class="text-drop"
							ondrop={onTextDrop}
							ondragover={onTextDragOver}
							onclick={() => textInput?.click()}
							aria-label="Enviar arquivo de texto"
						>
							<UploadIcon size={20} />
							<span>Clique para adicionar um arquivo de texto aqui</span>
							<small>Suporta <b>.txt/.pdf/.epub</b></small>
							<input
								type="file"
								accept=".txt,.pdf,.epub"
								bind:this={textInput}
								onchange={onTextFileChange}
								hidden
							/>
						</button>

						{#if textFileName}
							<div class="file-chip">
								<span>{textFileName}</span>
								<button
									type="button"
									class="icon-btn"
									onclick={() => {
										textFile = null;
										textFileName = '';
										bookForm.content = '';
									}}
									aria-label="Remover arquivo de texto"
								>
									<Trash2 size={16} />
								</button>
							</div>
						{/if}

						{#if bookForm.content && !textFile}
							<div class="content-preview">
								<label for="preview">Prévia do conteúdo (.txt)</label>
								<textarea id="preview" readonly
									>{bookForm.content.slice(0, 4000)}</textarea
								>
							</div>
						{/if}
					</div>
				</section>
			</div>

			<div class="modal-footer">
				<Button onclick={onClose} variant="outline" size="small">Fechar</Button>
				<Button size="small" onclick={handleSave}><BookOpen /> Adicionar</Button>
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
		min-height: 360px;
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
		margin-bottom: 0.75rem;
	}

	.text-upload {
		display: grid;
		gap: 0.5rem;
	}
	.text-drop {
		display: grid;
		place-items: center;
		gap: 0.35rem;
		border: 1px dashed var(--border-focus);
		border-radius: 10px;
		padding: 0.9rem;
		background: var(--background-white);
		cursor: pointer;
		text-align: center;
	}
	.text-drop small {
		color: var(--text-secondary);
	}

	.content-preview {
		display: grid;
		gap: 0.35rem;
	}
	.content-preview textarea {
		width: 100%;
		min-height: 140px;
		resize: vertical;
		padding: 0.6rem 0.7rem;
		border-radius: 8px;
		border: 1px solid var(--border);
		background: var(--background-white);
		font-family:
			ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New',
			monospace;
		white-space: pre-wrap;
	}

	.modal-footer {
		padding: 1rem 1.25rem;
		border-top: 1px solid var(--border-light);
		display: flex;
		justify-content: flex-end;
		gap: 0.75rem;
	}

	@media (max-width: 860px) {
		.content-grid {
			grid-template-columns: 1fr;
		}
		.cover-drop {
			min-height: 280px;
		}
		.form-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
