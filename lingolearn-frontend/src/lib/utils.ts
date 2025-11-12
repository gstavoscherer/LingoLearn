import { browser } from '$app/environment';
import JSZip from 'jszip';

// Carrega o PDFParse só no navegador
let PDFParse: any = null;

if (browser) {
	(async () => {
		const mod = await import('pdf-parse');
		PDFParse = mod.PDFParse;
		PDFParse.setWorker(
			'https://cdn.jsdelivr.net/npm/pdf-parse@latest/dist/pdf-parse/web/pdf.worker.mjs'
		);
	})();
}

export function EasinnessFactorToStarRating(factor: number): number {
	return Math.ceil(8 * factor - 11);
}

export function starRatingToLabel(rating: number): string {
	if (rating == 1 || rating == 0) return 'Nova';
	else if (rating == 2) {
		return 'Aprendendo';
	} else if (rating == 3) {
		return 'Aprendendo';
	} else if (rating == 4) {
		return 'Aprendendo';
	} else if (rating == 5) {
		return 'Dominado';
	} else {
		return '';
	}
}

export async function extractTextFromPDF(file: File): Promise<string> {
	if (!browser) {
		console.warn('extractTextFromPDF called in SSR — skipped.');
		return '';
	}

	if (!PDFParse) {
		const mod = await import('pdf-parse');
		PDFParse = mod.PDFParse;
		PDFParse.setWorker(
			'https://cdn.jsdelivr.net/npm/pdf-parse@latest/dist/pdf-parse/web/pdf.worker.mjs'
		);
	}

	try {
		// Lê o arquivo como ArrayBuffer
		const arrayBuffer = await file.arrayBuffer();
		const typedArray = new Uint8Array(arrayBuffer);

		const parser = new PDFParse({ data: typedArray });
		const result = await parser.getText();

		await parser.destroy();

		return result.text;
	} catch (error) {
		throw new Error(`Erro ao extrair texto do PDF: ${error}`);
	}
}

export async function extractTextFromEPUB(file: File): Promise<string> {
	try {
		const zip = new JSZip();
		const epub = await zip.loadAsync(file);

		let fullText = '';

		// Primeiro, encontrar o arquivo container.xml para entender a estrutura
		const containerFile = epub.file('META-INF/container.xml');
		if (!containerFile) {
			throw new Error('Arquivo EPUB inválido: container.xml não encontrado');
		}

		const containerContent = await containerFile.async('text');
		const rootfilePath = extractRootFilePath(containerContent);

		if (!rootfilePath) {
			throw new Error('Não foi possível encontrar o arquivo raiz do EPUB');
		}

		// Ler o arquivo de pacote (.opf) que contém a estrutura
		const opfFile = epub.file(rootfilePath);
		if (!opfFile) {
			throw new Error(`Arquivo OPF não encontrado: ${rootfilePath}`);
		}

		const opfContent = await opfFile.async('text');
		const contentFiles = await extractContentFiles(opfContent, epub, rootfilePath);

		// Processar cada arquivo de conteúdo
		for (const contentFile of contentFiles) {
			const content = await contentFile.async('text');
			const text = extractTextFromHTML(content);
			fullText += text + '\n\n';
		}

		return fullText.trim();
	} catch (error) {
		console.error('Erro ao extrair texto do EPUB:', error);
		throw new Error(`Erro ao extrair texto do EPUB: ${error}`);
	}
}

// Função auxiliar para extrair o caminho do arquivo raiz
function extractRootFilePath(containerXml: string): string | null {
	const match = containerXml.match(/full-path="([^"]+)"/);
	return match ? match[1] : null;
}

// Função auxiliar para extrair e carregar arquivos de conteúdo
async function extractContentFiles(
	opfContent: string,
	epub: JSZip,
	opfPath: string
): Promise<JSZip.JSZipObject[]> {
	const parser = new DOMParser();
	const opfDoc = parser.parseFromString(opfContent, 'application/xml');

	const manifestItems = opfDoc.querySelectorAll('manifest item');
	const contentFiles: JSZip.JSZipObject[] = [];

	// Determinar o diretório base do OPF
	const opfDir = opfPath.split('/').slice(0, -1).join('/');

	for (const item of manifestItems) {
		const mediaType = item.getAttribute('media-type');
		const href = item.getAttribute('href');

		// Processar apenas arquivos HTML/XHTML
		if (
			mediaType &&
			href &&
			(mediaType.includes('html') ||
				mediaType.includes('xhtml') ||
				mediaType === 'application/xhtml+xml')
		) {
			// Resolver caminho relativo
			const fullPath = opfDir ? `${opfDir}/${href}` : href;
			const contentFile = epub.file(fullPath);

			if (contentFile) {
				contentFiles.push(contentFile);
			}
		}
	}

	return contentFiles;
}

// Função auxiliar para extrair texto de HTML
function extractTextFromHTML(html: string): string {
	const parser = new DOMParser();
	const doc = parser.parseFromString(html, 'text/html');

	// Remover elementos que não contêm texto útil
	const elementsToRemove = doc.querySelectorAll('script, style, nav, header, footer');
	elementsToRemove.forEach((el) => el.remove());

	// Extrair texto
	const text = doc.body?.textContent || '';

	// Limpar e normalizar o texto
	return text
		.replace(/\s+/g, ' ')
		.replace(/[ \t]+/g, ' ')
		.trim();
}

export async function sendStudyTime(seconds: number, token: string) {
	try {
		const response = await fetch(`${import.meta.env.VITE_API_URL}/users/add-user-time?seconds=${seconds}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${token}`
			},
		});

		if (!response.ok) {
			console.error('Failed to send study time');
		} else {
			console.log(`Study time sent: ${seconds} seconds`);
		}
	} catch (error) {
		console.error('Error sending study time:', error);
	}
}

export function formatStudyTime(seconds: number): string {
	if (!seconds || seconds <= 0) return '0min';

	const hours = Math.floor(seconds / 3600);
	const minutes = Math.floor((seconds % 3600) / 60);

	if (hours === 0) {
		return `${minutes}min`;
	}

	return `${hours}h ${minutes.toString().padStart(2, '0')}min`;
}
