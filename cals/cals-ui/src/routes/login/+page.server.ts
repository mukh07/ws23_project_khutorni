import type { Actions } from './$types';
import { redirect } from '@sveltejs/kit';

export const actions = {
	default: async (event) => {
		const data = await event.request.formData();
		const username = data.get('username');
		const password = data.get('password');
		console.log(username, password);

		redirect(303, '/projects');
	}
} satisfies Actions;
