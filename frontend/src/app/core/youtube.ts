const VIDEO_ID = /^[A-Za-z0-9_-]{11}$/;

export function isVideoId(id: string | undefined | null): id is string {
  return !!id && VIDEO_ID.test(id);
}

export function thumbnailUrl(id: string): string {
  return isVideoId(id) ? `https://i.ytimg.com/vi/${id}/hqdefault.jpg` : '';
}

/** Privacy-enhanced embed URL; only called with IDs that passed isVideoId. */
export function embedUrl(id: string): string {
  return `https://www.youtube-nocookie.com/embed/${id}?rel=0&modestbranding=1`;
}
