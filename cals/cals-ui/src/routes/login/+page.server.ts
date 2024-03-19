import type { Actions } from './$types';
import { redirect } from '@sveltejs/kit';
import {fetcher} from "$lib/utils.js";

export const actions = {
	default: async (event) => {
		const data = await event.request.formData();
		const username = data.get('username');
		const password = data.get('password');

		const res = await fetcher(`/auth/login?username=${username}&password=${password}`, {
			method: "POST",
		});
		if (res.ok) {
			const { token } = await res.json();
			event.cookies.set('token', token, {
				secure: true,
				httpOnly: true,
				path: '/'
			});
			console.log(token)
		}

		redirect(303, '/projects');
	}
} satisfies Actions;
