import DOMPurify from 'isomorphic-dompurify';

export class InputSanitizer {
  static sanitizeHTML(input: string): string {
    return DOMPurify.sanitize(input, {
      ALLOWED_TAGS: [], //
      ALLOWED_ATTR: [],
    });
  }

  static validateFile(file: File, maxSize: number = 5 * 1024 * 1024): void {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];

    if (!allowedTypes.includes(file.type)) {
      throw new Error(
        'Invalid file type. Only JPEG, PNG, and WebP are allowed.',
      );
    }

    if (file.size > maxSize) {
      throw new Error(
        `File too large. Maximum size is ${maxSize / 1024 / 1024}MB.`,
      );
    }
  }

  // Sanitize URL inputs
  static validateURL(url: string): boolean {
    try {
      const parsedURL = new URL(url);
      const allowedProtocols = ['http:', 'https:'];
      return allowedProtocols.includes(parsedURL.protocol);
    } catch {
      return false;
    }
  }

  // Rate limiting for client
  static createRateLimiter(maxRequests: number, windowMs: number) {
    const requests = new Map();

    return (key: string): boolean => {
      const now = Date.now();
      const windowStart = now - windowMs;

      if (!requests.has(key)) {
        requests.set(key, []);
      }

      const userRequests = requests
        .get(key)
        .filter((time: number) => time > windowStart);

      if (userRequests.length >= maxRequests) {
        return false;
      }

      userRequests.push(now);
      requests.set(key, userRequests);
      return true;
    };
  }
}
