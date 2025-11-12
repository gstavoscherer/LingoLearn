import { type Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
	const flash = event.cookies.get('flash');

	if (flash) {
		event.locals.flash = JSON.parse(flash);
		event.cookies.delete('flash', { path: '/' });
	}

	return resolve(event);
};
