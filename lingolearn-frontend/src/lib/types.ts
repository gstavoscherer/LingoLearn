import type { Component } from 'svelte';

export type ToastVariant = 'success' | 'info' | 'warning' | 'error';

export type ToastType = {
	id: string;
	title: string;
	message: string;
	variant: ToastVariant;
};

export interface StatCardType {
	icon: Component;
	primary: string;
	secondary: string;
}

export interface SelectOptions {
	value: string;
	label: string;
}

export interface LanguageType {
	id: number;
	name: string;
	code: string;
}

export interface SidebarItemType {
	page?: string;
	callback?: (item: SidebarItemType) => void;
	label: string;
	icon: Component;
	isActive?: boolean;
	style?: 'blue' | 'red';
}

export interface PaginatedList<T> {
	items: T[];
	currentPage: number;
	totalPages: number;
	perPage: number;
	totalCount?: number;
}

export interface TextType {
	id: number;
	title: string;
	author: string;
	language: LanguageType;
	totalWords: number;
	totalKnownWords: number;
	lastVisitedPage: number;
	totalPages: number;
	imagePath?: string;
}

export interface PageType {
	id: number;
	textId: number;
	number: number;
	content: string;
}

export interface TextPageType {
	text: TextType;
	page: PageType;
}

export type WordStatus = 'unknown' | 'recognize' | 'familiar' | 'well-known' | 'known';

export type WordCategory = 'word' | 'punctuation';

export interface WordType {
	id?: number;
	word: string;
	languageId: number;
	category?: WordCategory;
	status?: WordStatus;
}

export interface UserWordType {
	id?: number;
	userId: number;
	word: WordType;
	easinessFactor: number;
	translation?: string;
	translationLanguageId: number;
	context: string;
	contextTranslation?: string;
	lastReview?: Date;
	nextReview?: Date;
	isNew: boolean;
}

export interface UserWordResponse {
	user_id: number;
	easiness_factor: number;
	translation: string;
	translation_language_id: number;
	context: string;
	context_translation: string;
	last_review?: string;
	next_review?: string;
	word: {
		id?: number;
		word: string;
		language_id: number;
		category?: string;
	};
}

export interface WordStats {
	total: number;
	known: number;
	learning: number;
	new: number;
}

export interface UserWordListResponse {
	pagination: PaginatedList<UserWordResponse>;
	stats: WordStats;
}

export interface DashboardData {
	userKnownWords: number;
	userKnownWordsLastWeek: number;
	streak: number;
	lastLogin: string | null;
	studyTimeToday: number;
}