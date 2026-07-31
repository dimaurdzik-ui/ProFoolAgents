export function logError(error: unknown): void {
  if (!process.env.PIXEL_AGENTS_INK_DEBUG_ERRORS) {
    return
  }

  console.error(error)
}
