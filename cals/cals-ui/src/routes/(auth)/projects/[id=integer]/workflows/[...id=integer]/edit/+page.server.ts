// export async function load

export const actions = {
  upsert: async ({ request }) => {
    const data = await request.formData();

    console.log(data)
  }
}