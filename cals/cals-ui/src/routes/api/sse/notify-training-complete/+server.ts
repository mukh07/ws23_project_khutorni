// src/routes/custom-event/+server.js
import { events } from 'sveltekit-sse'


export function POST({ request }) {
  return events({
    request,
    start({emit}) {
        emit('message', 'hello world')
      }
  })
}