// Identifies this browser tab. A tab ignores live events it sent itself,
// so incoming events don't overwrite what the host is typing.
export const clientId = Math.random().toString(36).slice(2) + Date.now().toString(36)

export default clientId
