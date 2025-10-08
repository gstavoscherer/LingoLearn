import type { Component } from 'svelte';

export type ToastVariant = 'success' | 'info' | 'warning' | 'error';

export type ToastType = {
	id: string;
	title: string;
	message: string;
    variant: ToastVariant
};

export interface SidebarItemType {
	page: string
	label: string
	icon: Component
	isActive?: boolean
	style?: 'blue' | 'red'
}

export interface TextType {
	id: number
	title: string
	author: string
	language: string
	totalWords: number
	totalKnowWords: number
	lastPage: number
	totalPages: number 
	imagePath?: string
}

export type WordStatus = 'unknown' | 'recognize' | 'familiar' | 'well-know' | 'know';

export type WordCategory =  'word' | 'punctuation';

export interface WordType {
	id?: number
	category: WordCategory
	status: WordStatus
	original: string
	translation?: string
	language?: string
}