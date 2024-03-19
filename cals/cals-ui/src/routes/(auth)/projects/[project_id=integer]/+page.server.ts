import {fetcher} from "$lib/utils.js";

export const actions = {
	default: async (event) => {
        console.log("Called form bg")
		const data = await event.request.formData();
		const name = data.get('name');
		const project_id = data.get('project_id');
		const batch_size = data.get('batch_size');
		const model = data.get('model');
		const description = data.get('description');
		const query_strategy = data.get('query_strategy');

		const res = await fetcher(
            `/projects/${project_id}`
                + `/workflows?name=${name}&batch_size=${batch_size}&model=${model}&description=${description}&query_strategy=${query_strategy}`, {
			method: "POST",
		}, event.cookies.get('token'));
		if (res.ok) {
			console.log(await res.json());
		}
	}
} satisfies Actions;
